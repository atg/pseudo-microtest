### -- Micro tests --
# Each tests one feature.
# If you're happy and you know it, print "ok".

# Good ideas from https://learnxinyminutes.com/docs/python3/
# See this gist for most core methods (excluding operators): https://gist.github.com/atg/7ae3b1aec988eb356887

# Some of the tests are from Python
# https://github.com/rfk/pypy/blob/master/lib-python/2.7/test/string_tests.py

## - Arithmetic -
# [arithmetic.add]
if 10 + 20 == 30: print("ok")

# [arithmetic.mul]
if 10 * 20 == 200: print("ok")

# [arithmetic.neg]
if -10 + 20 == 10: print("ok")

# [arithmetic.sub]
if 10 - 20 == -10: print("ok")

# [arithmetic.div]
if 20 / 10 == 2: print("ok")

# [arithmetic.rem]
if 5 % 2 == 1: print("ok")

# [arithmetic.pow]
if 3 ** 3 == 27: print("ok")



## - Logic -
# [logic.falsiness]
if "": print("not ok")
elif 0: print("not ok")
elif 0.0: print("not ok")
elif []: print("not ok")
elif {}: print("not ok")
elif set(): print("not ok")
elif None: print("not ok")
elif False: print("not ok")
else: print("ok")

# [logic.truthiness]
if "hello": print("ok")
if 10: print("ok")
if 3.14: print("ok")
if [1]: print("ok")
if {1}: print("ok")
if {"k": 1}: print("ok")
if True: print("ok")


# [logic.not]
if (not True) == False: print("ok")

# [logic.and]
if (True and False) == False: print("ok")

# [logic.or]
if (True or False) == True: print("ok")

# [logic.eq]
if 10 == 10: print("ok")
if "foo" == "fo" + "o": print("ok")

# [logic.neq]
if 10 != 20: print("ok")

# [logic.lt]
if 10 < 20: print("ok")

# [logic.gt]
if 20 > 10: print("ok")

# [logic.lteq]
if 10 <= 10: print("ok")

# [logic.gteq]
if 10 >= 10: print("ok")



## - Control Flow -
# [flow.for]
for x in range(10):
  if x == 9:
    print("ok")

# [flow.while]
while False:
  pass
print("ok")

# [flow.continue]
a = -1
for x in range(10):
  if x >= 5: continue
  a = x
if a == 4: print("ok")

# [flow.break]
a = -1
for x in range(10):
  a = x
  if x == 5: break
if a == 5: print("ok")

# [flow.ternary]
print("ok" if True else "not ok")
print("not ok" if False else "ok")


# [flow.elif]
if False:
  print("not ok")
elif True:
  print("ok")

# [flow.else]
if False:
  print("not ok")
else:
  print("ok")



## - Lists -
# [list.literal]
if [10, 20, 30][1] == 20: print("ok")

# [list.in]
if 10 in [10, 20, 30]: print("ok")

# [list.notin]
if 42 not in [10, 20, 30]: print("ok")

# [list.subscript_end]
if [10, 20, 30][-1] == 30: print("ok")

# [list.slice_az]
if [10, 20, 30, 40, 50][2:4] == [30, 40]: print("ok")

# [list.slice.a]
if [10, 20, 30, 40, 50][2:] == [30, 40, 50]: print("ok")

# [list.slice.z]
if [10, 20, 30, 40, 50][:4] == [10, 20, 30, 40]: print("ok")

# [list.pop]
xs = [10, 20, 30]
xs.pop()
if xs == [10, 20]: print("ok")

# [list.append]
xs = [10, 20, 30]
xs.append(40)
if xs == [10, 20, 30, 40]: print("ok")

# [list.extend]
xs = [10, 20]
xs.extend([30, 40])
if xs == [10, 20, 30, 40]: print("ok")

# [list.copy]
xs = [10, 20, 30, 40, 50]
ys = xs[:]
xs.pop()
if ys == [10, 20, 30, 40, 50]: print("ok")

# [list.del]
xs = [10, 20, 30]
del xs[0]
xs.pop()
if xs == [20, 30]: print("ok")

# [list.concat]
xs = [30, 40]
if [10, 20] + xs == [10, 20, 30, 40]: print("ok")

# [list.len]
if len([10, 20, 30]) == 3: print("ok")


## - Tuples -
# [tuple.in]
if 10 in (10, 20, 30): print("ok")

# [tuple.notin]
if 42 not in (10, 20, 30): print("ok")



## - Strings -
# [string.index]
if "hello"[1] == "e": print("ok")

# [string.concat]
if "hello" + "world" == "helloworld": print("ok")

# [string.repeat]
if "badger" * 3 == "badgerbadgerbadger": print("ok")


# [string.center_whitespace]
if "abc".center(10) == '   abc    ': print("ok")
if "".center(10) == '          ': print("ok")

# [string.center_fillchar]
if "abc".center(10, "z") == 'zzzabczzzz': print("ok")

# [string.endswith]
if "".endswith(""): print("ok") # All strings end with the empty string
if "a".endswith(""): print("ok")
if "a".endswith("a"): print("ok")
if "abcabc".endswith("abc"): print("ok")
if not "abcbc".endswith("abc"): print("ok")

# [string.expandtabs]
# Not sure if anybody uses this one.
if '\t'.expandtabs() == '        ': print("ok")
if '\t\t'.expandtabs(3) == '      ': print("ok")

# [string.find_1]
if 'abcdefghiabc'.find('abc') == 0: print("ok")
if 'abcdefghiabc'.find('abc', 1) == 9: print("ok")
if 'abcdefghiabc'.find('def', 4) == -1: print("ok")

if 'abc'.find('', 0) == 0: print("ok")
if 'abc'.find('', 3) == 3: print("ok")
if 'abc'.find('', 4) == -1: print("ok")

# [string.find_2]
if ''.find('') == 0: print("ok")
if ''.find('', 1, 1) == -1: print("ok")
if ''.find('', 42, 0) == -1: print("ok")

if ''.find('xx') == -1: print("ok")
if ''.find('xx', 1, 1) == -1: print("ok")
if ''.find('xx', 42, 0) == -1: print("ok")

# [string.rfind_1]
if 'abcdefghiabc'.rfind('abc') == 9: print("ok")
if 'abcdefghiabc'.rfind('') == 12: print("ok")
if 'abcdefghiabc'.rfind('abcd') == 0: print("ok")
if 'abcdefghiabc'.rfind('abcz') == -1: print("ok")

if 'abc'.rfind('', 0) == 3: print("ok")
if 'abc'.rfind('', 3) == 3: print("ok")
if 'abc'.rfind('', 4) == -1: print("ok")

# [string.format_bare]
if "he%so" % "ll" == "hello": print("ok")

# [string.format_tuple]
if "%se%so" % ("h", "ll") == "hello": print("ok")

# [string.index]
if 'abcdefghiabc'.index('') == 0: print("ok")
if 'abcdefghiabc'.index('def') == 3: print("ok")
if 'abcdefghiabc'.index('abc') == 0: print("ok")
if 'abcdefghiabc'.index('abc', 1) == 9: print("ok")

# [string.rindex]
if 'abcdefghiabc'.rindex('') == 12: print("ok")
if 'abcdefghiabc'.rindex('def') == 3: print("ok")
if 'abcdefghiabc'.rindex('abc') == 9: print("ok")
if 'abcdefghiabc'.rindex('abc', 0, -1) == 0: print("ok")

# [string.join]
if "X".join(['a', 'b', 'c']) == "aXbXc": print("ok")
if "".join(['a', 'b', 'c']) == "abc": print("ok")
if "X".join([]) == "": print("ok")
if "".join([]) == "": print("ok")


# [string.ljust]
if 'abc       ' == 'abc'.ljust(10): print("ok")
if 'abc   ' == 'abc'.ljust(6): print("ok")
if 'abc' == 'abc'.ljust(3): print("ok")
if 'abc' == 'abc'.ljust(2): print("ok")
if 'abc*******' == 'abc'.ljust(10, '*'): print("ok")

# [string.rjust]
if '       abc' == 'abc'.rjust(10): print("ok")
if '   abc' == 'abc'.rjust(6): print("ok")
if 'abc' == 'abc'.rjust(3): print("ok")
if 'abc' == 'abc'.rjust(2): print("ok")
if '*******abc' == 'abc'.rjust(10, '*'): print("ok")

# TODO: replace

# [string.partition]
if "abcdefcdxy".partition('cd') == ('ab', 'cd', 'efcdxy'): print("ok")
if "abcdefcdxy".rpartition('cd') == ('abcdef', 'cd', 'xy'): print("ok")
if "1234".partition('zw') == ('1234', '', ''): print("ok")
if "1234".rpartition('zw') == ('', '', '1234'): print("ok") # I hate this behaviour, but it's what Python does.

# [string.strip_whitespace]
if " badger ".strip() == "badger": print("ok")
if " badger ".lstrip() == "badger ": print("ok")
if " badger ".rstrip() == " badger": print("ok")

# [string.strip_characters]
if "XYbadgerYX".strip("XY") == "badger": print("ok")
if "XYbadgerYX".lstrip("XY") == "badgerYX": print("ok")
if "XYbadgerYX".rstrip("XY") == "XYbadger": print("ok")


# [string.split_whitespace]
if " a\tb\nc\rd\fe ".split() == ['a', 'b', 'c', 'd', 'e']: print("ok")

# [string.split]
if "XXaXXbXXcXXdXXeXX".split("XX") == ['', 'a', 'b', 'c', 'd', 'e', '']: print("ok")

# [string.split_maxsplit]
if "XXaXXbXXcXXdXXeXX".split("XX", 2) == ['', 'a', 'bXXcXXdXXeXX']: print("ok")
if "  a  b  c  d  e  ".split(maxsplit=2) == ['a', 'b', 'c  d  e  ']: print("ok")


# [string.splitlines]
if "".splitlines() == []: print("ok")
if "\n".splitlines() == [""]: print("ok")
if "\n\n".splitlines() == ["", ""]: print("ok")

if "\na".splitlines() == ["", "a"]: print("ok")
if "\na\n".splitlines() == ["", "a"]: print("ok")

if "".splitlines(True) == []: print("ok")
if "\n".splitlines(True) == ["\n"]: print("ok")
if "\n\n".splitlines(True) == ["\n", "\n"]: print("ok")

# [string.startswith]
if "".startswith(""): print("ok") # All strings start with the empty string
if "a".startswith(""): print("ok")
if "a".startswith("a"): print("ok")
if "abcabc".startswith("abc"): print("ok")
if not "bcabc".startswith("abc"): print("ok")

# [string.zfill]
if "".zfill(0) == "": print("ok")
if "".zfill(1) == "0": print("ok")
if "".zfill(3) == "000": print("ok")
if "abc".zfill(1) == "abc": print("ok")
if "abc".zfill(3) == "abc": print("ok")
if "abc".zfill(5) == "00abc": print("ok")

## - Sets -
# [set.in]
if 10 in {10, 20, 30}: print("ok")

# [set.notin]
if 10 not in {20, 30}: print("ok")

# [set.union]
if {20, 30} | {10, 20} == {10, 20, 30}: print("ok")

# [set.intersection]
if {20, 30} & {10, 20} == {20}: print("ok")

# [set.subsetof]
if {20, 30} <= {10, 20, 30}: print("ok")

# [set.supersetof]
if {10, 20, 30} >= {20, 30}: print("ok")



## - Variables -
# [var.int.immutable]
x = 6
y = 7
if x * y == 42: print('ok')

# [var.int.mutable]
x = 6
y = 7
x *= y
if x == 42 and y == 7: print('ok')

# [var.swap]
x = 10
y = 20
x, y = y, x
if x == 20 and y == 10: print("ok")



## - Yield -
# [yield]
def foo():
  for x in [10, 20, 30]:
    yield x * 2
if list(foo()) == [20, 40, 60]: print('ok')



## - Functions -
# [func.void_void]
def foo():
  print('ok')
foo()

# [func.int_void]
def foo(x: int):
  if x == 42:
    print('ok')
foo(42)

# [func.intint_void]
def foo(x: int, y: int):
  if x * y == 42:
    print('ok')
foo(6, 7)

# [func.intint_int]
def twice(x: int, y: int) -> int:
  return x * y
if twice(6, 7) == 42:
  print('ok')



## - Classes -
# [class.imethod.void_void]
class Barney:
  def __init__(self):
    pass
  def happyAndKnowsIt(self):
    print('ok')
barney = Barney()
barney.happyAndKnowsIt()

# [class.attributes]
class Barney:
  def __init__(self):
    self.status = 'ok'
  def happyAndKnowsIt(self):
    print(self.status)
barney = Barney()
barney.happyAndKnowsIt()
