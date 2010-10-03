Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Adding tasks:

  $ xt
  $ xt Sample one.
  $ xt
  3 - Sample one.
  $ xt Sample two.
  $ xt
  7 - Sample two.
  3 - Sample one.

Finishing tasks:

  $ xt -f 3
  $ xt
  7 - Sample two.
  $ xt -f 7
  $ xt

