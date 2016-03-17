### -- Micro tests --
# Each tests one feature.
# If you're happy and you know it, print "ok".

# Good ideas from https://learnxinyminutes.com/docs/python3/



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
if not True == False: print("ok")

# [logic.and]
if True and False == False: print("ok")

# [logic.or]
if True or False == True: print("ok")

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

# [string.format_bare]
if "he%so" % "ll" == "hello": print("ok")

# [string.format_tuple]
if "%se%so" % ("h", "ll") == "hello": print("ok")

# [string.concat]
if "hello" + "world" == "helloworld": print("ok")

# [string.repeat]
if "badger" * 3 == "badgerbadgerbadger": print("ok")

# [string.lrstrip]
if " badger ".strip() == "badger": print("ok")

# [string.lstrip]
if " badger ".lstrip() == "badger ": print("ok")

# [string.rstrip]
if " badger ".rstrip() == " badger": print("ok")



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
def foo(x: int, y: int) -> int:
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
