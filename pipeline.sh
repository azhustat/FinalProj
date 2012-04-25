#!/bin/sh

python pretag.py Han.txt

python preseg.py hanhansample.txt

javac SegMain.java
java SegMain preseg.txt

python postseg.py seg_result.txt
python score.py postseg.txt

cat ./Christine/CKaaTag.txt ./Christine/CKabTag.txt ./Christine/CKacTag.txt ./Christine/CKadTag.txt ./Christine/CKaeTag.txt ./Christine/CKafTag.txt ./Christine/CKagTag.txt ./Christine/CKahTag.txt ./Christine/CKaiTag.txt ./Christine/CKajTag.txt ./Siqi/SWaaTag.txt ./Siqi/SWabTag.txt ./Siqi/SWacTag.txt ./Siqi/SWadTag.txt ./Siqi/SWaeTag.txt ./Siqi/SWafTag.txt ./Siqi/SWagTag.txt ./Siqi/SWahTag.txt ./Siqi/SWaiTag.txt ./Siqi/SWajTag.txt ./Angie/AZaaTag.txt ./Angie/AZabTag.txt ./Angie/AZacTag.txt ./Angie/AZadTag.txt ./Angie/AZaeTag.txt ./Angie/AZafTag.txt ./Angie/AZagTag.txt ./Angie/AZahTag.txt ./Angie/AZaiTag.txt ./Angie/AZajTag.txt > sampletags.txt


python coocmat.py  postseg.txt
python condmat.py  postseg.txt
