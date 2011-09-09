Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Adding tasks:

  $ xt
  $ xt Sample one.
  $ xt
  3 - Sample one.
  $ xt Sample two.
  $ xt
  3 - Sample one.
  7 - Sample two.
  $ xt 'this | that'
  $ xt
  3 - Sample one.
  4 - this | that
  7 - Sample two.

Finishing tasks:

  $ xt -f 3
  $ xt
  4 - this | that
  7 - Sample two.
  $ xt -f 7
  $ xt
  4 - this | that
  $ xt -f 4
  $ xt

