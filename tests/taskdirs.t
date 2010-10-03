Setup:

  $ alias xt="python $TESTDIR/../t.py --list test"

Initialize multiple task directories:

  $ mkdir beer
  $ mkdir books
  $ xt --task-dir beer Dogfish Head 120 minute IPA
  $ xt --task-dir books Your Inner Fish
  $ xt --task-dir beer
  7 - Dogfish Head 120 minute IPA
  $ xt --task-dir books
  0 - Your Inner Fish

Wrong directories:

  $ xt --task-dir beer -f 0
  The ID "0" does not match any task.%
  $ xt --task-dir books -f 7
  The ID "7" does not match any task.%
  $ xt --task-dir beer
  7 - Dogfish Head 120 minute IPA
  $ xt --task-dir books
  0 - Your Inner Fish

Right directories:

  $ xt --task-dir beer -f 7
  $ xt --task-dir books -f 0
  $ xt --task-dir beer
  $ xt --task-dir books

