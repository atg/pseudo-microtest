import sys
import os
import subprocess
import re
import html
from re import compile as rx
from pprint import pprint
import json
import traceback

REMOVE_ANSI_RE = rx(r'\x1b[^m]*m')

def obj_to_json_html(obj):
  return html.escape(json.dumps(obj))

def setup_python_path():
  global PSEUDO_PATH, PSEUDOPYTHON_PATH
  # Laziness is the author's perogative
  if os.path.expanduser('~') == '/Users/alexgordon':
    PSEUDO_PATH = '/Users/alexgordon/temp/forks/pseudo' # TODO: don't hardcode path
    PSEUDOPYTHON_PATH = '/Users/alexgordon/temp/forks/pseudo-python'
  else:
    PSEUDO_PATH = os.path.abspath(sys.argv[1])
    PSEUDOPYTHON_PATH = os.path.abspath(sys.argv[2])
  
  sys.path.extend([PSEUDO_PATH, PSEUDOPYTHON_PATH])

setup_python_path()
import pseudo
import pseudo_python

# Some of the outputs have too much scrolling; narrow it down:
def preprocess_output(txt):
  txt = REMOVE_ANSI_RE.sub('', txt)
  
  p1 = PSEUDOPYTHON_PATH.rstrip('/')
  p2 = PSEUDO_PATH.rstrip('/')
  txt = txt.replace(p1, '[PSEUDO_PYTHON]')
  txt = txt.replace(p2, '[PSEUDO]')
  txt = txt.replace('Contents/MacOS/Python: ', 'Contents/MacOS/Python:\n  ')
  txt = txt.strip()
  if not txt:
    return '[no output received]'
  return txt

def run_at_path(ext, path):
  if   ext == 'py': args = ['python3', path]
  elif ext == 'rb': args = ['ruby', path]
  elif ext == 'js': args = ['node', path]
  elif ext == 'go': args = ['go', 'run', path]
  else:
    print("Cannot run this language (.%s) yet")
    assert False
  
  args.insert(0, '/usr/bin/env')
  return subprocess.check_output(args, stderr=subprocess.STDOUT)

def file_content_is(path, expected_content):
  try:
    with open(path, 'r') as f:
      return f.read() == expected_content
  except Exception:
    return False
    

microtests = []

LANGUAGES = [
  ("python", "py"),
  ("ruby", "rb"),
  ("javascript", "js"),
  ("go", "go"),
  # ("c#", "cs"),
  # ("c++", "cpp"),
  
  # python, ruby, javascript
  # c#, java
  # go, swift
  # c++, rust
  
]

class Microtest():
  def __init__(self, key, code):
    if '\n## ' in code:
      code = code.partition('\n## ')[0]
    
    assert '/' not in key
    self.key = key
    self.code = code
    self.statuses = {}
    
    self.global_errors = []
    self.codes = { ext: "" for lang, ext in LANGUAGES }
    self.errors = { ext: [] for lang, ext in LANGUAGES }
    self.statuses = {}
  
  
  # Make directories
  def make_dirs(self):
    self.dirname = 'microtests/%s' % self.key
    try:
      os.makedirs(self.dirname)
    except FileExistsError: pass
  
  # Create _original.py
  def generate_original_py(self):
    self.original_path = os.path.join(self.dirname, '_original.py')
    with open(self.original_path, 'w') as f:
      f.write(self.code)
  
  # Generate _original.pseudo.yaml
  def generate_yaml(self):
    self.pseudo_python_passed = False
    for lang, ext in LANGUAGES:
      self.statuses[ext] = 'bad'
    
    self.yaml_path = os.path.join(self.dirname, '_original.pseudo.yaml')
    # write to a file as an example and for debugging
    try:
      self.pseudo_ast = pseudo_python.translate_to_yaml(self.code)
      with open(self.yaml_path, 'w') as f:
        f.write(self.pseudo_ast)
      self.pseudo_python_passed = True
    except Exception as ex:
      self.pseudo_ast = None
      exc_type, exc_value, exc_traceback = sys.exc_info()
      self.global_errors.append({
        'kind': 'generate_yaml',
        'output': preprocess_output('\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))),
      })
  
  # Generate variations
  def generate_variations(self):
    if not self.pseudo_python_passed: return
    if self.pseudo_ast is None: return
    
    for lang, ext in LANGUAGES:
      try:
        output_path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
        self.codes[ext] = pseudo.generate_from_yaml(self.pseudo_ast, lang)
        with open(output_path, 'w') as f:
          f.write(self.codes[ext])
        print('~~ %s ~~' % ext)
      except Exception as e:
        print('~~ %s [error] ~~' % ext)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.errors[ext].append({
          'kind': 'generate_variations',
          'output': preprocess_output('\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))),
        })
        self.statuses[ext] = 'bad'
    
  def run_variations(self):
    original_output = run_at_path('py', self.original_path)
    
    if not self.pseudo_python_passed:
      return
    
    for lang, ext in LANGUAGES:
      path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
      print('Running %s code' % lang, path)
      
      try:
        try:
          with open(path, 'r') as f:
            self.codes[ext] = f.read()
        except Exception:
          pass
        
        txt = run_at_path(ext, path)
        lower_txt = txt.lower()
        
        # Push an error just in case
        self.errors[ext].append({
          'kind': 'run_variations_exit0',
          'output': preprocess_output(txt.decode('utf-8')),
        })
        self.statuses[ext] = 'bad'
      except subprocess.CalledProcessError as e:
        self.errors[ext].append({
          'kind': 'run_variations_exit1',
          'output': preprocess_output(e.output.decode('utf-8')),
        })
        self.statuses[ext] = 'bad'
        continue
      except Exception:
        self.statuses[ext] = 'bad'
        continue
      
      print('Testing!', self.key)
      print('original:', repr(original_output))
      print('passed:', repr(txt))
      
      if original_output == txt:
        self.statuses[ext] = 'good'
      elif txt.count(b'\n') > 4:
        self.statuses[ext] = 'bad'
      elif b'error' in lower_txt or b'exception' in lower_txt:
        self.statuses[ext] = 'bad'
      else:
        self.statuses[ext] = 'warn'
      
      if self.statuses[ext] == 'good':
        # Miraculously nothing went wrong. Pop the error we created
        self.errors[ext].pop()
  
  def status(self, lang, ext):
    'Status of a given language'
    if ext not in self.statuses:
      return 'untested'
    else:
      return self.statuses[ext]


TEST_NAME_RE = rx(r'^#[ \t]*\[([^\]\n]+)\][ \t]*$', re.MULTILINE)
def main():
  # set cwd to script directory
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  
  with open('microtests.py') as f:
    txt = f.read()
    assert '\r' not in txt
    
    tests = TEST_NAME_RE.split(txt)
    for i, test in enumerate(tests):
      if i == 0: continue # ignore the file header
      if i % 2 == 1: continue # ignore individual test headers
      
      key = tests[i - 1]
      code = test.strip() + '\n'
      
      # Assert that the tests are not empty
      if not key: continue
      if code == '\n': continue
      
      microtests.append(Microtest(key, code))
  
  assert microtests
  
  print("there are %d tests" % len(microtests))
  print(pseudo)
  
  # global microtests
  # microtests = microtests[:3]
  for mt in microtests:
    mt.make_dirs()
    mt.generate_original_py()
    mt.generate_yaml()
    mt.generate_variations()
    mt.run_variations()
    
    print('Errors for:' + mt.key)
    print(len(mt.global_errors))
    print({ext: len(mt.errors[ext]) for lang, ext in LANGUAGES})
  
  html_code = '\n'.join(generateHTML())
  print("OUTPUT")
  print(html_code)
  with open('html/output.html', 'w') as f:
    f.write(html_code)

def generateHTML():
  STATUS_SYMBOLS = {
    'untested': '❔',
    'good': '✅',
    'warn': '⚠️',
    'bad': '❌',
  }
  yield '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>pseudo microtests</title>
  
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
  <link href="style.css" rel="stylesheet" type="text/css">
  
  <!-- <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/themes/prism-tomorrow.min.css" rel="stylesheet" type="text/css"> -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/themes/prism.min.css" rel="stylesheet" type="text/css">
  
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/components/prism-javascript.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/components/prism-ruby.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/components/prism-python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.4.1/components/prism-go.min.js"></script>
  
<script>
$(function() {
  $(".mt_status").click(function() {
    var hljslang = $(this).attr("hljslang");
    var source_code = JSON.parse($(this).attr("source_code"));
    var generated_source_code = JSON.parse($(this).attr("generated_source_code"));
    
    var global_errors = JSON.parse($(this).attr("global_errors"));
    var errors = JSON.parse($(this).attr("errors"));
    
    function makeCodeBlock(code, lang) {
      if (!code || !code.length) {
        return $("<pre><em>No code was generated because an error occurred in pseudo-python. (see below)</em></pre>")[0];
      }
      var pre = $("<pre>");
      var code = $("<code>").addClass("language-" + lang).text(code);
      pre.append(code);
      return pre[0];
    }
    
    $("#errors").empty();
    $("#errors").append($("<h3>Code: original.py</h3>"));
    $("#errors").append(makeCodeBlock(source_code, "python"));
    
    $("#errors").append($("<h3>Code: generated</h3>"));
    $("#errors").append(makeCodeBlock(generated_source_code, hljslang));
    
    if (global_errors.length || errors.length) {
      $("#errors").append($("<h3>Errors</h3>"));
      function pushErrors(errs) {
        var kids = [];
        errs.forEach(function(err) {
          kids.push($("<b>").text(err.kind));
          kids.push($("<pre>").text(err.output));
        });
        $("#errors").append(kids);
      }
      
      pushErrors(global_errors);
      pushErrors(errors);
    }
    
    Prism.highlightAll();
  });
});
</script>

</head>
<body>
  <div id="errors"><b>&larr; Click on an icon to see the results for that test.</b></div>
  <table id="maintable">
    <tr class="mt_top">
      <th class="testname">Test Name</th>
  '''
  for lang, ext in LANGUAGES:
    yield '<td>%s</td>' % html.escape(lang)
  
  yield '</tr>'
  
  for mt in microtests:
    yield '<tr>'
    yield '<td class="mt_side">%s</td>' % (html.escape(mt.key))
    for lang, ext in LANGUAGES:
      status = mt.status(lang, ext)
      symbol = STATUS_SYMBOLS[status]
      yield '<td class="mt_status mt_status_%s" global_errors="%s" errors="%s" source_code="%s" generated_source_code="%s" hljslang="%s">%s</td>' % (
        html.escape(status),
        obj_to_json_html(mt.global_errors),
        obj_to_json_html(mt.errors[ext]),
        obj_to_json_html(mt.code),
        obj_to_json_html(mt.codes.get(ext)),
        html.escape(lang),
        html.escape(symbol))
    yield '</tr>'
  
  yield '''
  </table>
</body>
</html>
  '''
  
if __name__ == '__main__':
  main()
