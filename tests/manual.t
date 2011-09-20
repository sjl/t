Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Create a task file manually (no IDs):

  $ cat >> test << EOF
  > Sample one.
  > Sample two.
  > EOF
  $ xt
  3 - Sample one.
  7 - Sample two.

Add some manual tasks:

  $ echo 'Custom one. | id: custom1' >> test
  $ echo 'Custom two. | id: custom2' >> test
  $ xt
  3       - Sample one.
  7       - Sample two.
  custom1 - Custom one.
  custom2 - Custom two.

Rewrite the task file:

  $ cat > test << EOF
  > New.
  > EOF
  $ xt
  5 - New.

Add comments to task file:

  $ echo '# this is a comment' >> test
  $ xt
  5 - New.
