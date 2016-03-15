import sys
import os
import subprocess
import re
import html
from re import compile as rx
from pprint import pprint

def setup_python_path():
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
    try:
      subprocess.check_call([
        '/usr/bin/env', 'PYTHONPATH=%s:%s' % (PSEUDO_PATH, PSEUDOPYTHON_PATH), 'python3',
        os.path.join(PSEUDOPYTHON_PATH, 'pseudo_python', 'main.py'),
        self.original_path,
      ])
    except subprocess.CalledProcessError:
      pass
  
  # Generate variations
  def generate_variations(self):
    try:
      for lang, ext in LANGUAGES:
        print('~~ %s ~~' % ext)
        subprocess.check_call([
          '/usr/bin/env', 'PYTHONPATH=%s:%s' % (PSEUDO_PATH, PSEUDOPYTHON_PATH), 'python3',
          os.path.join(PSEUDOPYTHON_PATH, 'pseudo_python', 'main.py'),
          '_original.py',
          '%s.%s' % (self.key, ext),
        ], cwd=os.path.abspath(self.dirname))
    except subprocess.CalledProcessError:
      pass
  
  def run_variations(self):
    self.statuses = {}
    original_output = run_at_path('py', self.original_path)
    
    for lang, ext in LANGUAGES:
      path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
      print('Running %s code' % lang, path)
      
      try:
        txt = run_at_path(ext, path)
        lower_txt = txt.lower()
      except Exception:
        self.statuses[ext] = 'bad'
        continue
      
      if original_output == txt:
        self.statuses[ext] = 'good'
      elif txt.count(b'\n') > 4:
        self.statuses[ext] = 'bad'
      elif b'error' in lower_txt or b'exception' in lower_txt:
        self.statuses[ext] = 'bad'
      else:
        self.statuses[ext] = 'warn'
  
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
  
  for mt in microtests:
    mt.make_dirs()
    mt.generate_original_py()
    mt.generate_yaml()
    mt.generate_variations()
    mt.run_variations()
  
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
</head>
<body>
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
      yield '<td class="mt_status mt_status_%s">%s</td>' % (html.escape(status), html.escape(symbol))
    yield '</tr>'
  
  yield '''
  </table>
</body>
</html>
  '''
  
if __name__ == '__main__':
  main()
