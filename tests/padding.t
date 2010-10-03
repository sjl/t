Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Add tasks of varying width:

  $ xt Short.
  $ xt Longcat is long.

Test paddings:

  $ xt
  4 - Longcat is long.
  5 - Short.
  $ cat test
  Longcat is long. | id:4c623ab4df5cc1a10d32558768c2c21bddf2c053
  Short. | id:5a7a65db2caa6313a70ceb75b1bd806f7879f6b7
  $ cat >> test << EOF
  > Long one. | id: long1
  > Very long two. | id: long2
  > EOF
  $ xt -f 5
  $ xt
  4     - Longcat is long.
  long1 - Long one.
  long2 - Very long two.
  $ cat test
  Longcat is long. | id:4c623ab4df5cc1a10d32558768c2c21bddf2c053
  Long one. | id:long1
  Very long two. | id:long2
