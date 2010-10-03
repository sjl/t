Setup:

  $ alias xt="python $TESTDIR/../t.py --task-dir `pwd` --list test"

Add some tasks manually:

  $ cat > test << EOF
  > One | id: 1
  > Two. | id: 2
  > Zero. | id: 0
  > Three. | id: 3
  > A. | id: a
  > B. | id: b
  > AA. | id: aa
  > CC. | id: cc
  > EOF

Make sure they're sorted correctly in the output:

  $ xt
  0  - Zero.
  1  - One
  2  - Two.
  3  - Three.
  a  - A.
  aa - AA.
  b  - B.
  c  - CC.

Make sure the file hasn't actually changed:

  $ cat test
  One | id: 1
  Two. | id: 2
  Zero. | id: 0
  Three. | id: 3
  A. | id: a
  B. | id: b
  AA. | id: aa
  CC. | id: cc

