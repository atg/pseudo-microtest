import sys
import os
import subprocess
import re
import html
from re import compile as rx
from pprint import pprint
import json

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


# Some of the outputs have too much scrolling; narrow it down:
def preprocess_output(txt):
  p1 = PSEUDOPYTHON_PATH.rstrip('/')
  p2 = PSEUDO_PATH.rstrip('/')
  txt = txt.replace(p1, '[PSEUDO_PYTHON]')
  txt = txt.replace(p2, '[PSEUDO]')
  txt = txt.replace('Contents/MacOS/Python: ', 'Contents/MacOS/Python:\n  ')
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
  # ("c++", "cpp"),
]

class Microtest():
  def __init__(self, key, code):
    assert '/' not in key
    self.key = key
    self.code = code
    self.statuses = {}
    self.global_errors = []
    self.errors = { ext: [] for lang, ext in LANGUAGES }
  
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
    try:
      subprocess.check_output([
        '/usr/bin/env', 'PYTHONPATH=%s:%s' % (PSEUDO_PATH, PSEUDOPYTHON_PATH), 'python3',
        os.path.join(PSEUDOPYTHON_PATH, 'pseudo_python', 'main.py'),
        self.original_path,
      ], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      self.global_errors.append({
        'kind': 'generate_yaml',
        'output': preprocess_output(e.output.decode('utf-8')),
      })
    self.pseudo_python_passed = True
  
  # Generate variations
  def generate_variations(self):
    for lang, ext in LANGUAGES:
      try:
        print('~~ %s ~~' % ext)
        output = subprocess.check_output([
          '/usr/bin/env', 'PYTHONPATH=%s:%s' % (PSEUDO_PATH, PSEUDOPYTHON_PATH), 'python3',
          os.path.join(PSEUDOPYTHON_PATH, 'pseudo_python', 'main.py'),
          '_original.py',
          '%s.%s' % (self.key, ext),
          
          # os.path.join(PSEUDO_PATH, 'pseudo', 'main.py'),
          # '_original.pseudo.yaml',
          # '_original.py',
          # '%s.%s' % (self.key, ext),
          
        ], cwd=os.path.abspath(self.dirname), stderr=subprocess.STDOUT)
      except subprocess.CalledProcessError as e:
        self.errors[ext].append({
          'kind': 'generate_variations',
          'output': preprocess_output(e.output.decode('utf-8')),
        })
  
  def run_variations(self):
    self.statuses = {}
    original_output = run_at_path('py', self.original_path)
    
    for lang, ext in LANGUAGES:
      path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
      print('Running %s code' % lang, path)
      
      try:
        txt = run_at_path(ext, path)
        lower_txt = txt.lower()
        
        # Push an error just in case
        self.errors[ext].append({
          'kind': 'run_variations_exit0',
          'output': preprocess_output(txt.decode('utf-8')),
        })
      except subprocess.CalledProcessError as e:
        self.errors[ext].append({
          'kind': 'run_variations_exit1',
          'output': preprocess_output(e.output.decode('utf-8')),
        })
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
  # microtests = microtests[:5]
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

<script>
$(function() {
  $(".mt_status").click(function() {
    var source_code = JSON.parse($(this).attr("source_code"));
    var global_errors = JSON.parse($(this).attr("global_errors"));
    var errors = JSON.parse($(this).attr("errors"));
    
    $("#errors").empty();
    $("#errors").append($("<h3>Code: original.py</h3>"));
    $("#errors").append($("<pre>").text(source_code));
    
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
  });
});
</script>

</head>
<body>
  <div id="errors"></div>
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
      yield '<td class="mt_status mt_status_%s" global_errors="%s" errors="%s" source_code="%s">%s</td>' % (
        html.escape(status),
        obj_to_json_html(mt.global_errors),
        obj_to_json_html(mt.errors[ext]),
        obj_to_json_html(mt.code),
        html.escape(symbol))
    yield '</tr>'
  
  yield '''
  </table>
</body>
</html>
  '''
  
if __name__ == '__main__':
  main()
