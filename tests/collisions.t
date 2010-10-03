Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Make some tasks that collide in their first letter:

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
  $ xt
  0  - 9
  3  - 1
  1b - 4
  7b - 12
  fe - 8
  bd - 13
  77 - 3
  c  - 6
  9  - 7
  b1 - 10
  a  - 5
  fa - 14
  17 - 11
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
  bd  - 13
  d   - 2
  ee  - 1test
  fe  - 8
  77  - 3
  2   - 5test
  14  - 6test
  35  - 1
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
  5   - 2test
  c1  - 6
  ac  - 5

