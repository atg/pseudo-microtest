### -- Micro tests --
# Each tests one feature.
# If you're happy and you know it, print "ok".

# Good ideas from https://learnxinyminutes.com/docs/python3/
# See this gist for most core methods (excluding operators): https://gist.github.com/atg/7ae3b1aec988eb356887

# Some of the tests are from PyPy
# https://github.com/rfk/pypy/blob/master/lib-python/2.7/test/string_tests.py


## - Integers -
# [int.add]
if 10 + 20 == 30: print("ok")

# [int.mul]
if 10 * 20 == 200: print("ok")

# [int.neg]
if -10 + 20 == 10: print("ok")

# [int.sub]
if 10 - 20 == -10: print("ok")

# [int.div]
if 20 / 10 == 2: print("ok")

# [int.rem]
if 5 % 2 == 1: print("ok")

# [int.precedence]
if 3 ** 5 * 7 + 11 ** 2 * 13 == 3274: print("ok")

# [int.mod]
# -1 is congruent to 1 (mod 2)
if (-1) % 2 == 1: print("ok")

# There are no negative integers in Z/nZ!
# For languages that don't implement modulo division properly, you'll need a function such as
#   function _correct_mod_int(a: int, b: int) -> int {
#     return ((a % b) + b) % b);
#   }

# [int.pow]
if 3 ** 3 == 27: print("ok")

# [int.abs]
if abs(-3) == 3: print("ok")

# [int.bitwise]
if 23 | 51 == 55: print("ok1")
if 23 & 51 == 19: print("ok2")
if 23 ^ 51 == 36: print("ok3")
if 23 << 3 == 184: print("ok4")
if 23 >> 2 == 5: print("ok5")
if -23 << 3 == -184: print("ok6")
if -23 >> 2 == -6: print("ok7")

## - Floats -
# [float.arithmetic]
if 29.0 < 10.0 + 20.0 < 31.0: print("ok add")
if -11.0 < 10.0 - 20.0 < -9.0: print("ok sub/neg")
if 199.0 < 10.0 * 20.0 < 201.0: print("ok mul")
if 1.0 < 20 / 10 < 3.0: print("ok div")

# [float.fmod]
if 0.5 < 2.4 % 1.8 < 0.65: print("ok fmod positive")
if 0.5 < (-1.8) % 2.4 < 0.65: print("ok fmod negative")

# [float.comparison]
if 0.1 == 0.1: print("ok eq 1")
if 0.1 != 0.2: print("ok neq")

if 0.1 < 0.2: print("ok lt 1")
if not (0.1 < 0.1): print("ok lt 2")

if 0.2 > 0.1: print("ok gt 1")
if not (0.1 > 0.1): print("ok gt 2")

if 0.1 <= 0.1: print("ok lteq 1")
if 0.1 <= 0.2: print("ok lteq 2")

if 0.1 >= 0.1: print("ok lteq 1")
if 0.2 >= 0.2: print("ok lteq 2")

# [float.subnormal]
# I'm not particularly attached to these tests, feel free to ignore them.
if 0.00000000000000000000000000000000000000001 != 0.0: print("ok subnormal is not 0")
if 0.00000000000000000000000000000000000000001 == 0.00000000000000000000000000000000000000001: print("ok subnormal self equal")


## - Logic -
# [logic.falsiness]
if "": print("not ok 1")
elif 0: print("not ok 2")
elif 0.0: print("not ok 3")
elif []: print("not ok 4")
elif {}: print("not ok 5")
elif set(): print("not ok 6")
elif None: print("not ok 7")
elif False: print("not ok 8")
else: print("ok")

# [logic.truthiness]
if "hello": print("ok1")
if 10: print("ok2")
if 3.14: print("ok3")
if [1]: print("ok4")
if {1}: print("ok5")
if {"k": 1}: print("ok6")
if True: print("ok7")


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

## - Comprehensions -
# [list.comprehension]
xs = [1, 2, 3, 4, 5]
ys = [x * 5 for x in xs if x % 2 == 1]
for y in ys:
  print("%d" % y)

# [set.comprehension]
xs = [1, 2, 3, 4, 5]
ys = {x * 5 for x in xs if x % 2 == 1}
print("%d" % sum(ys))

# [dict.comprehension]
xs = ["a", "b", "c", "d", "e"]
ys = {x: x for x in xs if x != 'c'}
print(ys['a'])
print(ys['b'])
print(ys['d'])
print(ys['e'])


# [generator.comprehension]
xs = [1, 2, 3, 4, 5]
ys = (x * 5 for x in xs if x % 2 == 1)
for y in ys:
  print("%d" % y)


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

# [list.del]
xs = [10, 20, 30]
del xs[0]
xs.pop()
if xs == [20, 30]: print("ok")

# [list.__add__]
xs = [30, 40]
if [10, 20] + xs == [10, 20, 30, 40]: print("ok")

# [list.__len__]
if len([10, 20, 30]) == 3: print("ok")


# [list.append]
xs = [10, 20, 30]
xs.append(40)
if xs == [10, 20, 30, 40]: print("ok")

# [list.copy_1]
xs = [10, 20, 30, 40, 50]
ys = xs[:]
xs.pop()
if ys == [10, 20, 30, 40, 50]: print("ok")

# [list.copy_2]
xs = [10, 20, 30, 40, 50]
ys = xs.copy()
xs.pop()
if ys == [10, 20, 30, 40, 50]: print("ok")

# [list.clear]
xs = [10, 20, 30, 40, 50]
xs.clear()
if not xs: print("ok")

# [list.count]
if [10].count(10) == 1: print("ok")
if [10, 20, 10].count(10) == 2: print("ok")

# [list.extend]
xs = [10, 20]
xs.extend([30, 40])
if xs == [10, 20, 30, 40]: print("ok")

# [list.insert]
xs = [10, 30]
xs.insert(1, 20)
if xs == [10, 20, 30]: print("ok")

# [list.index]
xs = [10, 20, 30, 20]
if xs.index(20) == 1: print("ok")

# [list.pop]
xs = [10, 20, 30]
xs.pop()
if xs == [10, 20]: print("ok")

# [list.remove]
xs = [10, 20, 30, 10]
xs.remove(10)
if xs == [20, 30, 10]: print("ok")

# [list.reverse]
xs = [10, 20, 30]
xs.reverse()
if xs == [30, 20, 10]: print("ok")

# [list.sort]
xs = [20, 30, 10, -10]
xs.sort()
if xs == [-10, 10, 20, 30]: print("ok")


# TODO: list#sort(key=, reverse=)

## - Tuples -
# [tuple.in]
if 10 in (10, 20, 30): print("ok")

# [tuple.notin]
if 42 not in (10, 20, 30): print("ok")

# [tuple.count]
if (10,).count(10) == 1: print("ok1")
if (10, 20, 10,).count(10) == 2: print("ok2")


## - Strings -
# [string.__getitem__]
if "hello"[1] == "e": print("ok")

# [string.__add__]
if "hello" + "world" == "helloworld": print("ok")

# [string.__mul__]
if "badger" * 3 == "badgerbadgerbadger": print("ok")

# [string.__len__]
if len("") == 0: print("ok1")
if len("abc") == 3: print("ok2")

# [string.center_whitespace]
if "abc".center(10) == '   abc    ': print("ok1")
if "".center(10) == '          ': print("ok2")

# [string.center_fillchar]
if "abc".center(10, "z") == 'zzzabczzzz': print("ok")

# [string.endswith]
if "".endswith(""): print("ok1") # All strings end with the empty string
if "a".endswith(""): print("ok2")
if "a".endswith("a"): print("ok3")
if "abcabc".endswith("abc"): print("ok4")
if not "abcbc".endswith("abc"): print("ok5")

# [string.expandtabs]
# Not sure if anybody uses this one.
if '\t'.expandtabs() == '        ': print("ok1")
if '\t\t'.expandtabs(3) == '      ': print("ok2")

# [string.find_1]
if 'abcdefghiabc'.find('abc') == 0: print("ok1")
if 'abcdefghiabc'.find('abc', 1) == 9: print("ok2")
if 'abcdefghiabc'.find('def', 4) == -1: print("ok3")

if 'abc'.find('', 0) == 0: print("ok1")
if 'abc'.find('', 3) == 3: print("ok2")
if 'abc'.find('', 4) == -1: print("ok3")

# [string.find_2]
if ''.find('') == 0: print("ok1")
if ''.find('', 1, 1) == -1: print("ok2")
if ''.find('', 42, 0) == -1: print("ok3")

if ''.find('xx') == -1: print("ok1")
if ''.find('xx', 1, 1) == -1: print("ok2")
if ''.find('xx', 42, 0) == -1: print("ok3")

# [string.rfind_1]
if 'abcdefghiabc'.rfind('abc') == 9: print("ok1")
if 'abcdefghiabc'.rfind('') == 12: print("ok2")
if 'abcdefghiabc'.rfind('abcd') == 0: print("ok3")
if 'abcdefghiabc'.rfind('abcz') == -1: print("ok4")

if 'abc'.rfind('', 0) == 3: print("ok1")
if 'abc'.rfind('', 3) == 3: print("ok2")
if 'abc'.rfind('', 4) == -1: print("ok3")

# [string.format_bare]
if "he%so" % "ll" == "hello": print("ok")

# [string.format_tuple]
if "%se%so" % ("h", "ll") == "hello": print("ok")

# [string.index]
if 'abcdefghiabc'.index('') == 0: print("ok1")
if 'abcdefghiabc'.index('def') == 3: print("ok2")
if 'abcdefghiabc'.index('abc') == 0: print("ok3")
if 'abcdefghiabc'.index('abc', 1) == 9: print("ok4")

# [string.rindex]
if 'abcdefghiabc'.rindex('') == 12: print("ok1")
if 'abcdefghiabc'.rindex('def') == 3: print("ok2")
if 'abcdefghiabc'.rindex('abc') == 9: print("ok3")
if 'abcdefghiabc'.rindex('abc', 0, -1) == 0: print("ok4")

# [string.join]
if "X".join(['a', 'b', 'c']) == "aXbXc": print("ok1")
if "".join(['a', 'b', 'c']) == "abc": print("ok2")
if "X".join([]) == "": print("ok3")
if "".join([]) == "": print("ok4")


# [string.ljust]
if 'abc       ' == 'abc'.ljust(10): print("ok1")
if 'abc   ' == 'abc'.ljust(6): print("ok2")
if 'abc' == 'abc'.ljust(3): print("ok3")
if 'abc' == 'abc'.ljust(2): print("ok4")
if 'abc*******' == 'abc'.ljust(10, '*'): print("ok5")

# [string.rjust]
if '       abc' == 'abc'.rjust(10): print("ok1")
if '   abc' == 'abc'.rjust(6): print("ok2")
if 'abc' == 'abc'.rjust(3): print("ok3")
if 'abc' == 'abc'.rjust(2): print("ok4")
if '*******abc' == 'abc'.rjust(10, '*'): print("ok5")

# TODO: replace

# [string.partition]
if "abcdefcdxy".partition('cd') == ('ab', 'cd', 'efcdxy'): print("ok1")
if "abcdefcdxy".rpartition('cd') == ('abcdef', 'cd', 'xy'): print("ok2")
if "1234".partition('zw') == ('1234', '', ''): print("ok3")
if "1234".rpartition('zw') == ('', '', '1234'): print("ok4") # I hate this behaviour, but it's what Python does.

# [string.strip_whitespace]
if " badger ".strip() == "badger": print("ok1")
if " badger ".lstrip() == "badger ": print("ok2")
if " badger ".rstrip() == " badger": print("ok3")

# [string.strip_characters]
if "XYbadgerYX".strip("XY") == "badger": print("ok1")
if "XYbadgerYX".lstrip("XY") == "badgerYX": print("ok2")
if "XYbadgerYX".rstrip("XY") == "XYbadger": print("ok3")


# [string.split_whitespace]
if " a\tb\nc\rd\fe ".split() == ['a', 'b', 'c', 'd', 'e']: print("ok")

# [string.split]
if "XXaXXbXXcXXdXXeXX".split("XX") == ['', 'a', 'b', 'c', 'd', 'e', '']: print("ok")

# [string.split_maxsplit]
if "XXaXXbXXcXXdXXeXX".split("XX", 2) == ['', 'a', 'bXXcXXdXXeXX']: print("ok1")
if "  a  b  c  d  e  ".split(maxsplit=2) == ['a', 'b', 'c  d  e  ']: print("ok2")


# [string.splitlines]
if "".splitlines() == []: print("ok1")
if "\n".splitlines() == [""]: print("ok2")
if "\n\n".splitlines() == ["", ""]: print("ok3")

if "\na".splitlines() == ["", "a"]: print("ok4")
if "\na\n".splitlines() == ["", "a"]: print("ok5")

if "".splitlines(True) == []: print("ok6")
if "\n".splitlines(True) == ["\n"]: print("ok7")
if "\n\n".splitlines(True) == ["\n", "\n"]: print("ok8")

# [string.startswith]
if "".startswith(""): print("ok1") # All strings start with the empty string
if "a".startswith(""): print("ok2")
if "a".startswith("a"): print("ok3")
if "abcabc".startswith("abc"): print("ok4")
if not "bcabc".startswith("abc"): print("ok5")

# [string.zfill]
if "".zfill(0) == "": print("ok1")
if "".zfill(1) == "0": print("ok2")
if "".zfill(3) == "000": print("ok3")
if "abc".zfill(1) == "abc": print("ok4")
if "abc".zfill(3) == "abc": print("ok5")
if "abc".zfill(5) == "00abc": print("ok6")

## - Sets -
# [set.__eq__]
if {1, 2} == {2, 1}: print("ok")

# [set.in]
if 10 in {10, 20, 30}: print("ok")

# [set.not_in]
if 10 not in {20, 30}: print("ok")

# [set.difference]
if {20, 30} - {10, 20} == {30}: print("ok")
if {20, 30}.difference({10, 20}) == {30}: print("ok")

# [set.union]
if {20, 30} | {10, 20} == {10, 20, 30}: print("ok")
if {20, 30}.union({10, 20}) == {10, 20, 30}: print("ok")

# [set.intersection]
if {20, 30} & {10, 20} == {20}: print("ok")
if {20, 30}.intersection({10, 20}) == {20}: print("ok")

# [set.symmetric_difference]
if {10, 20} ^ {20, 30} == {10, 30}: print("ok")
if {10, 20}.symmetric_difference({20, 30}) == {10, 30}: print("ok")

# TODO: set#difference_update
# TODO: set#intersection_update
# TODO: set#symmetric_difference_update



# [set.issubset]
if {20, 30} <= {30, 20}: print("ok1")
if {20, 30} <= {10, 20, 30}: print("ok2")
if {20, 30}.issubset({30, 20}): print("ok3")
if {20, 30}.issubset({10, 20, 30}): print("ok4")

# [set.issuperset]
if {20, 30} >= {30, 20}: print("ok1")
if {10, 20, 30} >= {30, 20}: print("ok2")
if {20, 30}.issuperset({30, 20}): print("ok3")
if {10, 20, 30}.issuperset({30, 20}): print("ok4")

# [set.proper_subsetof]
if not ({10, 20} < {20, 10}): print("ok1")
if {10, 20} < {20, 10, 30}: print("ok2")

# [set.proper_supersetof]
if not ({10, 20} > {20, 10}): print("ok1")
if {10, 20, 30} > {20, 10}: print("ok2")

# [set.__iter__]
xs = {"ok"}
for x in xs:
  print(x)

# [set.add]
xs = {10}
xs.add(10)
xs.add(20)
if xs == {20, 10}: print("ok")

# [set.clear]
xs = {10, 20}
xs.clear()
if len(xs) == 0: print("ok")

# [set.copy]
xs = {10, 20}
ys = xs.copy()
xs.clear()
if ys == {20, 10}: print("ok")


# [set.discard]
xs = {10, 20}
xs.discard(20)
xs.discard(42)
if xs == {10}: print("ok")


# [set.isdisjoint]
if set().isdisjoint(set()): print("ok1")
if {10}.isdisjoint(set()): print("ok2")
if set().isdisjoint({10}): print("ok3")
if {10}.isdisjoint({42}): print("ok4")
if not {40, 20, 10}.isdisjoint({10, 20, 30}): print("ok5")

# [set.pop]
xs = {10, 20, 30}
xs.pop()
if len(xs) == 2: print("ok")

# [set.remove]
xs = {10, 20, 30}
xs.remove(20)
if xs == {30, 10}: print("ok")

# [set.update]
xs = {10, 20, 30}
xs.update({40, 30, 20})
if xs == {10, 40, 20, 30}: print("ok")



## - Dictionaries -
# [dict.in]
xs = {}
if 'k' not in xs: print("ok")

xs = { 'k1': True, 'k2': False }
if 'k2' in xs: print("ok")

# TODO: dict#get(k[,default])
# TODO: dict#pop(k[,default])
# TODO: dict#setdefault(k[,default])
# TODO: dict#update([other, ]**kwargs)


# [dict.__iter__]
xs = { "a": "b" }
for k in xs:
  print(k)

# [dict.items]
xs = { "a": "b" }
for k, v in xs.items():
  print(k)
  print(v)

# [dict.keys]
xs = { "a": "b" }
for k in xs.keys():
  print(k)

# [dict.values]
xs = { "a": "b", "c": "b" }
for v in xs.values():
  print(v)


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

# [class.public_attributes]
class Barney:
  def __init__(self):
    self.status = 'not ok'
barney = Barney()
barney.status = "ok"
print(barney.status)

# [class.public_static_attributes]
class Barney:
  status = 'not ok'
Barney.status = "ok"
print(Barney.status)

# [class.class_method.void_void]
class Barney:
  def __init__(self):
    pass
  @classmethod
  def happyAndKnowsIt(klass):
    print("ok")
Barney.happyAndKnowsIt()

# [class.static_method.void_void]
class Barney:
  def __init__(self):
    pass
  @staticmethod
  def happyAndKnowsIt():
    print("ok")
Barney.happyAndKnowsIt()


## - Standard Library -
# https://docs.python.org/dev/library/index.html

# [this file is getting a bit long, so it might be sensible to split it up

# Most commonly used Python libraries:
#  string
#  re
#  
#  datetime
#  calendar
#  collections
#  array
#  copy
#  pprint
#  enum
#  
#  math
#  cmath
#  decimal
#  fractions
#  random
#  statistics
#  
#  itertools
#  functools
#  operator
#  
#  shutil
#  
#  sqlite3
#  hashlib
#  
#  os
#  io
#  time
#  argparse
#  
#  subprocess
#  
#  json
#  base64
#  
#  html
#  xml.dom.minidom
#  
#  uuid
#  traceback

## - Third Party Libraries -
#  requests




## - Random -
# [lib.random.randint]
import random
if 10 <= random.randint(10, 11) <= 11:
  print("ok 1")
if random.randint(10, 10) == 10:
  print("ok 2")

# TODO: more random tests

## - Time -
# [lib.time.time]
import time
t = time.time()
if int(t) == t: print("not ok")
t2 = int(t)
print("the current time is roughly %d" % (t2 - t2 % 100))

# TODO: more time tests
# [lib.time.sleep

## - JSON -
# [lib.json.dumps]
import json
print(json.dumps([1, 2, 3]))

# [lib.json.loads]
import json
if json.loads("[1, 2, 3]") == [1, 2, 3]: print("ok")

# TODO: json.dump() and json.load(), and all the options to dumps, dump, loads, load




# Tests that don't exist yet:
# Files
#   file.___

# - Process/Filesystem -
# https://docs.python.org/dev/library/os.html
# [lib.os.environ
# [lib.os.chdir
# [lib.os.fchdir
# [lib.os.getcwd
# [lib.os.getenv
# [lib.os.getegid
# [lib.os.geteuid
# [lib.os.getgid
# [lib.os.getlogin
# [lib.os.getpgid
# [lib.os.getpgrp
# [lib.os.getpid
# [lib.os.getppid
# [lib.os.getuid
# [lib.os.putenv
# ...etc

# - Regex -
# https://docs.python.org/dev/library/re.html
# [lib.re.search
# [lib.re.match
# [lib.re.fullmatch
# [lib.re.split
# [lib.re.findall
# [lib.re.finditer
# [lib.re.sub
# [lib.re.subn

# [lib.re.match.group
# [lib.re.match.groups
# [lib.re.match.groupdict
# [lib.re.match.start
# [lib.re.match.end
# [lib.re.match.span


# - Subprocess -
# https://docs.python.org/dev/library/subprocess.html
# [lib.subprocess.check_call
# [lib.subprocess.check_output

# - IO -
# https://docs.python.org/dev/library/io.html
# [lib.io.stringio]

