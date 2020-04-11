Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Replace a task's text (preserving the ID):

  $ xt Sample.
  a
  $ xt
  a - Sample.
  $ xt -e a New sample.
  $ xt
  d - New sample.
  $ xt 'this | that'
  4
  $ xt
  4 - this | that
  d - New sample.
  $ xt -e 4 'this &| that'
  $ xt
  d1 - this &| that
  df - New sample.

Sed-style substitution:

  $ xt -e a 's/New/Testing/'
  error: the ID "a" does not match any task
  [1]
  $ xt
  d1 - this &| that
  df - New sample.
  $ xt -e 4 '/this &/this /'
  error: the ID "4" does not match any task
  [1]
  $ xt
  d1 - this &| that
  df - New sample.

