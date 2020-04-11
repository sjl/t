Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Adding tasks:

  $ xt
  $ xt Sample one.
  3
  $ xt
  3 - Sample one.
  $ xt Sample two.
  7
  $ xt
  3 - Sample one.
  7 - Sample two.
  $ xt 'this | that'
  4
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

Output when adding in various modes:

  $ xt foo
  0
  $ xt -v bar
  62cdb7020ff920e5aa642c3d4066950dd1f01f4d
  $ xt -q baz
