#!/bin/sh
python preseg.py jlsample.txt
javac SegMain.java
java SegMain preseg.txt
python postseg.py seg_result.txt