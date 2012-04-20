#!/bin/sh
python preseg.py Hanhan.txt

javac SegMain.java
java SegMain preseg.txt

python postseg.py seg_result.txt
python score.py postseg.txt