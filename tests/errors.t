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
  7 - Sample two.
  3 - Sample one.

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
  35 - 1
  1b - 4
  32 - Sample one.
  7a - Sample two.
  bd - 13
  77 - 3
  c  - 6
  9  - 7
  b1 - 10
  a  - 5
  7b - 12
  fa - 14
  17 - 11
  fe - 8
  d  - 2

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
  0a  - 9
  5   - 2test
  d   - 2
  ee  - 1test
  fe  - 8
  77  - 3
  2   - 5test
  14  - 6test
  35  - 1
  32  - Sample one.
  90  - 7
  8   - 12test
  b1d - 10
  17  - 11
  a1  - 7test
  7b  - 12
  c7  - 13test
  07  - 8test
  36  - 4test
  6   - 11test
  0e  - 9test
  b10 - 10test
  95  - 3test
  fa  - 14
  1b  - 4
  ef  - 14test
  7a  - Sample two.
  bd  - 13
  c1  - 6
  ac  - 5
  $ xt -f b1
  The ID "b1" matches more than one task.%
  $ xt -e b1
  The ID "b1" matches more than one task.%
  $ xt
  0a  - 9
  5   - 2test
  d   - 2
  ee  - 1test
  fe  - 8
  77  - 3
  2   - 5test
  14  - 6test
  35  - 1
  32  - Sample one.
  90  - 7
  8   - 12test
  b1d - 10
  17  - 11
  a1  - 7test
  7b  - 12
  c7  - 13test
  07  - 8test
  36  - 4test
  6   - 11test
  0e  - 9test
  b10 - 10test
  95  - 3test
  fa  - 14
  1b  - 4
  ef  - 14test
  7a  - Sample two.
  bd  - 13
  c1  - 6
  ac  - 5

