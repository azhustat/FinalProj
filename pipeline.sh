#!/bin/sh

python pretag.py Han.txt

python preseg.py hanhansample.txt

javac SegMain.java
java SegMain preseg.txt

python postseg.py seg_result.txt
python score.py postseg.txt