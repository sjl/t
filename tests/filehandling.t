Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Add a task file:

  $ ls -a
  .
  ..
  $ xt
  $ ls -a
  .
  ..
  $ xt Sample.
  $ ls -a
  .
  ..
  .test.done
  test

Finish a task without deleting:

  $ xt -f a
  $ ls -a
  .
  ..
  .test.done
  test

Finish a task with deleting:

  $ xt Another.
  $ xt --delete-if-empty -f c
  $ ls -a
  .
  ..
  .test.done

