Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Add some test tasks:

  $ xt Sample one.
  $ xt Sample two.

Bad prefix:

  $ xt -f BAD
  The ID "BAD" does not match any task.%
  $ xt -e BAD This should not be replaced.
  The ID "BAD" does not match any task.%
  $ xt
  3 - Sample one.
  7 - Sample two.

Ambiguous identifiers:

  $ xt 1
  $ xt 2
  $ xt 3
  $ xt 4
  $ xt 5
  $ xt 6
  $ xt 7
  $ xt 8
  $ xt 9
  $ xt 10
  $ xt 11
  $ xt 12
  $ xt 13
  $ xt 14
  $ xt -f 1
  The ID "1" matches more than one task.%
  $ xt -f e This should not be replaced.
  The ID "e" does not match any task.%
  $ xt
  0  - 9
  17 - 11
  1b - 4
  32 - Sample one.
  35 - 1
  77 - 3
  7a - Sample two.
  7b - 12
  9  - 7
  a  - 5
  b1 - 10
  bd - 13
  c  - 6
  d  - 2
  fa - 14
  fe - 8

Even more ambiguity:

  $ xt 1test
  $ xt 2test
  $ xt 3test
  $ xt 4test
  $ xt 5test
  $ xt 6test
  $ xt 7test
  $ xt 8test
  $ xt 9test
  $ xt 10test
  $ xt 11test
  $ xt 12test
  $ xt 13test
  $ xt 14test
  $ xt
  07  - 8test
  0a  - 9
  0e  - 9test
  14  - 6test
  17  - 11
  1b  - 4
  2   - 5test
  32  - Sample one.
  35  - 1
  36  - 4test
  5   - 2test
  6   - 11test
  77  - 3
  7a  - Sample two.
  7b  - 12
  8   - 12test
  90  - 7
  95  - 3test
  a1  - 7test
  ac  - 5
  b10 - 10test
  b1d - 10
  bd  - 13
  c1  - 6
  c7  - 13test
  d   - 2
  ee  - 1test
  ef  - 14test
  fa  - 14
  fe  - 8
  $ xt -f b1
  The ID "b1" matches more than one task.%
  $ xt -e b1
  The ID "b1" matches more than one task.%
  $ xt
  07  - 8test
  0a  - 9
  0e  - 9test
  14  - 6test
  17  - 11
  1b  - 4
  2   - 5test
  32  - Sample one.
  35  - 1
  36  - 4test
  5   - 2test
  6   - 11test
  77  - 3
  7a  - Sample two.
  7b  - 12
  8   - 12test
  90  - 7
  95  - 3test
  a1  - 7test
  ac  - 5
  b10 - 10test
  b1d - 10
  bd  - 13
  c1  - 6
  c7  - 13test
  d   - 2
  ee  - 1test
  ef  - 14test
  fa  - 14
  fe  - 8

