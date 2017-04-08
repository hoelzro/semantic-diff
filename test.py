import unittest

import semantic_diff

class SemanticDiffTests(unittest.TestCase):
    def assertSemanticallySame(self, before, after):
        pass

    def assertSemanticallyDifferent(self, before, after):
        pass

    def test_import_aliasing(self):
        self.assertSemanticallySame('''
import foo

foo.bar()
''',
'''
import foo as f

f.bar()
''')

    def test_local_importing(self):
        self.assertSemanticallySame('''
import foo

foo.bar()
''',
'''
from foo import bar

bar()
''')

    def test_reorder_independent_functions(self):
        self.assertSemanticallySame('''
def foo():
    pass

def bar():
    pass
''',
'''
def bar():
    pass

def foo():
    pass
''')

    def test_override_local_import(self):
        self.assertSemanticallyDifferent('''
from foo import bar

bar()
''',
'''
from foo import bar

bar = 17

bar()
''')

    def test_override_local_import_noop_ok(self):
        self.assertSemanticallySame('''
from foo import bar

bar()
''',
'''
from foo import bar

bar = bar

bar()
''')

    def test_override_local_assignment_flow(self):
        # any assignments to bar shouldn't affect the result either, unless they're function calls
        self.assertSemanticallySame('''
from foo import bar

bar()
''',
'''
import foo
from foo import bar

baz = foo.bar
bar = baz

baz()
''')

    def test_local_import_plus_change(self):
        self.assertSemanticallyDifferent('''
import foo

bar = 17

foo.bar()
''',
'''
from foo import bar

bar = 17

bar()
''')

    @unittest.skip
    def test_dont_update_descriptive_comment(self):
        # XXX this won't work using the built-in AST library

        self.assertSemanticallyDifferent('''
# some comment that describes the next line
next_line()
''',
'''
# some comment that describes the next line
prev_line()
>>>>>>>>
''')

    def test_add_new_function(self):
        self.assertSemanticallyDifferent('''
def foo():
  pass
''',
'''
def foo():
  pass

def bar():
  pass
''')


    def test_change_variable_name(self):
        self.assertSemanticallySame('''
a = 17
print a
''',
'''
b = 17
print b
''')

    def test_refactor_lift(self):
        self.assertSemanticallySame('''
def complicated_function():
    do()
    something()
    complicated()

    # this is a hack for $REASON
    giant()
    hacky()
    code()
''',
'''
def hacky_thing():
    giant()
    hacky()
    code()

def complicated_function():
    do()
    something()
    complicated()

    hacky_thing()
''')


    def test_unused_import(self):
        self.assertSemanticallySame('''
print 'Hello, World!'
''',
'''
import foo

print 'Hello, World!'
''')
