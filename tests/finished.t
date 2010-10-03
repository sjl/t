Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Add some tasks:

  $ xt Sample one.
  $ xt Sample two.
  $ xt Sample three.
  $ xt Sample four.

Finish and test .test.done:

  $ xt -f 1
  $ cat .test.done
  Sample four. | id:1dd56b09a9ca0fdf4f2a8c0959a298098eb8f7de
  $ xt -f 7
  $ cat .test.done
  Sample four. | id:1dd56b09a9ca0fdf4f2a8c0959a298098eb8f7de
  Sample two. | id:7a4dc18c23f3b890602da09da1690ccfb4c87bd1
  $ xt -f 3
  $ cat .test.done
  Sample four. | id:1dd56b09a9ca0fdf4f2a8c0959a298098eb8f7de
  Sample one. | id:329950673481cb1c19102c982bfc63e745ab4a6f
  Sample two. | id:7a4dc18c23f3b890602da09da1690ccfb4c87bd1
  $ xt -f 9
  $ cat .test.done
  Sample four. | id:1dd56b09a9ca0fdf4f2a8c0959a298098eb8f7de
  Sample one. | id:329950673481cb1c19102c982bfc63e745ab4a6f
  Sample two. | id:7a4dc18c23f3b890602da09da1690ccfb4c87bd1
  Sample three. | id:90cf0626ca134e0aa6453b3562dc1c8bb34f1568

