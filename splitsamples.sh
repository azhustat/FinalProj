#!/bin/sh

head -n 3000 hanhanweibo.txt > hanhansample.txt

head -n 1000 hanhanweibo.txt |tail -n 1000 >./Christine/CKsamples.txt
head -n 2000 hanhanweibo.txt |tail -n 1000 >./Siqi/SWsamples.txt
head -n 3000 hanhanweibo.txt |tail -n 1000 >./Angie/AZsamples.txt

cd ./Christine
split -l 100 CKsamples.txt CK

cd ../Siqi
split -l 100 SWsamples.txt SW

cd ../Angie
split -l 100 AZsamples.txt AZ




tail -n 1000 hanhanweibo.txt >./TestSet/testsamples.txt
cd ./TestSet/
split -l 100 testsamples.txt testset
mv testsetaa testsetaa.txt
mv testsetab testsetab.txt
mv testsetac testsetac.txt
mv testsetad testsetad.txt
mv testsetae testsetae.txt
mv testsetaf testsetaf.txt
mv testsetag testsetag.txt
mv testsetah testsetah.txt
mv testsetai testsetai.txt
mv testsetaj testsetaj.txt


head -n 500 testsamples.txt > testsamples500.txt

python testsetpreseg.py testsamples500.txt

javac SegMain.java
java SegMain testsetpreseg.txt

python testsetpostseg.py seg_result.txt
python testsetscore.py testsetpostseg.txt



python testsetpostscore.py testsetpostseg.txt

python tsfreqmat.py testsetpostscore.txt 


cat testsetaaTag.txt testsetabTag.txt testsetacTag.txt testsetadTag.txt testsetaeTag.txt > testsettags.txt

