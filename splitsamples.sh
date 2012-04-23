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

