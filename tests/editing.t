Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Replace a task's text (preserving the ID):

  $ xt Sample.
  $ xt
  a - Sample.
  $ xt -e a New sample.
  $ xt
  a - New sample.

Sed-style substitution:

  $ xt -e a 's/New/Testing/'
  $ xt
  a - Testing sample.

