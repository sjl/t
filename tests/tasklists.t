Setup:

  $ alias xt="python $TESTDIR/../t.py --list `pwd`"

Initialize multiple task lists:

  $ xt --list beer Dogfish Head 120 minute IPA
  7
  $ xt --list books Your Inner Fish
  0
  $ xt --list beer
  7 - Dogfish Head 120 minute IPA
  $ xt --list books
  0 - Your Inner Fish

Wrong lists:

  $ xt --list beer -f 0
  error: the ID "0" does not match any task
  [1]
  $ xt --list books -f 7
  error: the ID "7" does not match any task
  [1]
  $ xt --list beer
  7 - Dogfish Head 120 minute IPA
  $ xt --list books
  0 - Your Inner Fish

Right lists:

  $ xt --list beer -f 7
  $ xt --list books -f 0
  $ xt --list beer
  $ xt --list books

