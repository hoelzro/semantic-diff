import unittest

import semantic_diff

class SemanticDiffTests(unittest.TestCase):
    def test_import_aliasing(self):
```
<<<<<<<<
import foo

foo.bar()
========
import foo as f

f.bar()
>>>>>>>>
```

    def test_local_importing(self):
```
<<<<<<<<
import foo

foo.bar()
========
from foo import bar

bar()
>>>>>>>>
```

    def test_reorder_independent_functions(self):
```
<<<<<<<<
def foo():
    pass

def bar():
    pass
========
def bar():
    pass

def foo():
    pass
>>>>>>>>
```

    def test_override_local_import(self):
```
# DIFFERS
<<<<<<<<
from foo import bar

bar()
========
from foo import bar

bar = 17

bar()
>>>>>>>>
```

    def test_override_local_import_noop_ok(self):
```
<<<<<<<<
from foo import bar

bar()
========
from foo import bar

bar = bar

bar()
>>>>>>>>
```

    def test_override_local_assignment_flow(self):
```
# DOESN'T DIFFER
<<<<<<<<
from foo import bar

bar()
========
import foo
from foo import bar

baz = foo.bar
# any assignments to bar shouldn't affect the result either, unless they're function calls
bar = baz

baz()

>>>>>>>>
```

    def test_local_import_plus_change(self):
```
# DIFFERS
<<<<<<<<
import foo

bar = 17

foo.bar()
========
from foo import bar

bar = 17

bar()
>>>>>>>>
```

    # XXX this won't work using the built-in AST library
    @unittest.skip
    def test_dont_update_descriptive_comment(self):

```
# DIFFERS
<<<<<<<<
# some comment that describes the next line
next_line()
========
# some comment that describes the next line
prev_line()
>>>>>>>>
```

    def test_add_new_function(self):
```
# DIFFERS
<<<<<<<<
def foo():
  pass
========
def foo():
  pass

def bar():
  pass
>>>>>>>>
```

What if the function/variable/import is not used?  Things to keep in mind:

  * Some imports have side effects - this is pretty damn uncommon, though
  * Decorators on functions and classes can have side effects!
  * Classes and functions at a module top level are implicitly exported, so they may be used outside of this module


    def test_change_variable_name(self):
```
<<<<<<<<
a = 17
print a
========
b = 17
print b
>>>>>>>>
```

    def test_refactor_lift(self):
```
# KIND OF DIFFERS
<<<<<<<<
def complicated_function():
    do()
    something()
    complicated()

    # this is a hack for $REASON
    giant()
    hacky()
    code()
========
def hacky_thing():
    giant()
    hacky()
    code()

def complicated_function():
    do()
    something()
    complicated()

    hacky_thing()
>>>>>>>>
```


    def test_unused_import(self):
```
<<<<<<<<
...
========
import foo

...
>>>>>>>>
```
