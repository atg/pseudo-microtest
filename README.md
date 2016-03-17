# pseudo-microtest

Small tests for [pseudo](https://github.com/alehander42/pseudo)

## Understanding

Inside `microtests.py` are 40+ tests of language features. e.g. the first two tests are

```py
# [arithmetic.add]
if 10 + 20 == 30: print("ok")

# [arithmetic.mul]
if 10 * 20 == 200: print("ok")
```

**pseudo-microtest** compiles each individual test into a YAML file using pseudo-python. Then it converts each YAML file into Ruby, JavaScript, Go, and back into Python. It then runs each microtest (and the original Python test), and compares the output.

The final task of **pseudo-microtest** is to generate a pretty HTML table of the results of each test.


## Prereqs

The point of this tool is to test pseudo with a lot of languages, so you'll need a lot of interpreters installed.

1. Python 3: `brew install python3`

2. Ruby

3. node.js

4. golang: `brew install go`


## Usage

1. Clone both [pseudo](https://github.com/alehander42/pseudo-python) and [pseudo-python](https://github.com/alehander42/pseudo-python)

2. Run `python3 main.py <path/to/pseudo> <path/to/pseudo-python>`

3. Open `html/output.html`


## Technologies

HTML output uses `highlight.js` for highlighting

## Screenshots

![a screenshot showing a table with red, yellow and green cells corresponding to errors/warnings and ok and expanded case line with outputs and translations for each language](http://i.imgur.com/K9rzsPF.png)
