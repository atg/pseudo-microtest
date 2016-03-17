import sys
import os
import subprocess
import re
import html
from re import compile as rx
from pprint import pprint

def setup_python_path():
    if len(sys.argv) > 2:
        PSEUDO_PATH = os.path.abspath(sys.argv[1])
        PSEUDO_PYTHON_PATH = os.path.abspath(sys.argv[2])
        sys.path.extend([PSEUDO_PATH, PSEUDO_PYTHON_PATH])

setup_python_path()
import pseudo
import pseudo_python

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
    # ("c#", "cs")
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
        yaml_path = os.path.join(self.dirname, '_original.pseudo.yaml')
        # write to a file as an example and for debugging
        try:
            self.pseudo_ast = pseudo_python.translate_to_yaml(self.code)
            with open(yaml_path, 'w') as f:
                f.write(self.pseudo_ast)
        except Exception as ex:
            self.pseudo_ast = None
            self.variations = {}
            self.outputs = {}
            for lang, ext in LANGUAGES:
                self.variations[ext] = 'PSEUDO-PYTHONERROR:<br>%s' % str(ex)
                self.outputs[ext] = ''

    # Generate variations
    def generate_variations(self):
        if self.pseudo_ast is None:
            return
        self.variations = {}
        for lang, ext in LANGUAGES:
            try:
                output_path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
                self.variations[ext] = pseudo.generate_from_yaml(self.pseudo_ast, lang)
                with open(output_path, 'w') as f:
                    f.write(self.variations[ext])
                print('~~ %s ~~' % ext)
            except Exception as e:
                self.variations[ext] = 'TRANSLATE ERROR:<br>%s' % str(e)
    
    def run_variations(self):
        self.statuses = {}
        self.original_output = run_at_path('py', self.original_path)
        self.outputs = {}

        for lang, ext in LANGUAGES:
            path = os.path.join(self.dirname, '%s.%s' % (self.key, ext))
            if not self.pseudo_ast or self.variations[ext].startswith('TRANSLATE ERROR:'):
                self.outputs[ext] = ''
                self.statuses[ext] = 'bad'
                continue

            print('Running %s code' % lang, path)
            
            try:
                txt = run_at_path(ext, path)
                lower_txt = txt.lower()
            except Exception as e:
                self.statuses[ext] = 'bad'
                self.outputs[ext] = 'RUN ERROR:<br>%s' % str(e.output.decode('utf-8'))
                continue
            
            self.outputs[ext] = txt.decode('utf-8')
            if self.original_output == txt:
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
        yield '<tr class="statuses">'
        yield '<td class="mt_side">%s</td>' % (html.escape(mt.key))
        for lang, ext in LANGUAGES:
            status = mt.status(lang, ext)
            symbol = STATUS_SYMBOLS[status]
            yield '<td class="mt_status mt_status_%s">%s</td>' % (html.escape(status), html.escape(symbol))
        yield '</tr>'

        yield '<tr class="results">'
        yield '<td><div><pre>%s____</pre></div></td>' % mt.original_output.decode('utf-8')
        for lang, ext in LANGUAGES:
            yield '<td><div><pre>%s____</pre></div></td>' % mt.outputs[ext]
        yield '</tr>'

        yield '<tr class="languages">'
        yield '<td><pre><code class="python">%s</code></pre></td>' % mt.code
        for lang, ext in LANGUAGES:
            yield '<td><div><pre><code class=%s>%s</code></pre></div></td>' % (html.escape(lang), mt.variations[ext])
        yield '</tr>'
    
    yield '''
    </table>
    <script type='text/javascript' src='output.js'>
    </script>
</body>
</html>
    '''
    
if __name__ == '__main__':
    main()
