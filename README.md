# Semantic Diff

This implements a Python module that performs a *semantic diff* on two chunks of Python code.  By "semantic diff",
I mean that changes that it deems to result in code that does the exact same thing are ignored.  This isn't just
whitespace and comment changes - it's also things like independent loads.  For example:

```python
a = 1
b = 2
print a
```

If you swap the first two lines, the functionality doesn't change, since the two assignments are independent of
one another.  Another example:

```python
a = 1
b = a
print b
```

This is considered equivalent to the first example, since we're still printing 1!

# Demo

[![asciicast](https://asciinema.org/a/3vtwwc9e90whfhxi5ed394k7g.png)](https://asciinema.org/a/3vtwwc9e90whfhxi5ed394k7g)

# Usage

I'm not going to provide usage documentation from Python just yet - this is a work in progress enough as it is!

To use it from the command line, grab a copy (`git clone https://github.com/hoelzro/semantic-diff`), throw
it in your `PYTHONPATH`, and run it like so:

    python2 -m semantic_diff before.py after.py

It's VERY much a work in progress, so I expect it to explode on pretty much anything except for trivial examples
like the ones shown above.

I'll clean it up and make it easier to use as time goes on.

# Rules of Thumb

  1. If you don't know or can't tell, two things are non-equivalent.
  2. Functions are considered impure and side-effectful. (I might add the ability to mark functions as pure later)
  3. Importing a module doesn't have side effects (most don't - I might add the ability to contradict this rule later)
