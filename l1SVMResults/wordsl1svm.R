#library(penalizedSVM);
label = read.table("selectedwords.txt")$V1;

freqmat <- data.matrix(read.table("freqmat.txt", header=FALSE))
tags = read.table("sampletags.txt")$V1
library(lpRegPath)

#y = tags;
#y[y==0] = -1;
#y[y==9] = -1;
print("doing a l1 norm svm...");
#l1svmPathPos = path.svm.L1(y, t(freqmat), intercept=TRUE)
#library(penalizedSVM)
#svmPos = lpsvm(t(freqmat), y, k = 0, nu = 0.2, output = 1, delta = 10^-3, epsi = 10^-4,seed = 123, maxIter=50)

#l1svmCVPos = risk.svm.L1(y, t(freqmat), intercept=TRUE, 
#                          fold=2, repetition=1)

# 1. L1Norm SVM word image for the positive class:
# create the new tag vector: +1 for positive class; -1 for all other classes
beta = readMat("./lpsvmPosResult.mat")$w;
rownames(beta) <- label
# top absolute coefficient values:

print("#############positive class####################")
num = 20
word =label[order(abs(beta),decreasing=T)][1:num];
coefficient = sort(abs(beta),decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top positive coefficient values:
#print(sort(beta,decreasing=T)[1:num])
word =label[order(beta,decreasing=T)][1:num];
coefficient = sort(beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top negative coefficient values:
#print(sort(-beta,decreasing=T)[1:num])
word =label[order(-beta,decreasing=T)][1:num];
coefficient = sort(-beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);

# 2. L1Norm SVM word image for the negative class:
# create the new tag vector: +1 for negative class; -1 for all other classes
beta = readMat("./lpsvmNegResult.mat")$w;
rownames(beta) <- label
# top absolute coefficient values:
print("#############negative class####################")
word =label[order(abs(beta),decreasing=T)][1:num];
coefficient = sort(abs(beta),decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top positive coefficient values:
word =label[order(beta,decreasing=T)][1:num];
coefficient = sort(beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top negative coefficient values:
word =label[order(-beta,decreasing=T)][1:num];
coefficient = sort(-beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);

# 3. L1Norm SVM word image for the neutral class:
# create the new tag vector: +1 for neutral class; -1 for all other classes
beta = readMat("./lpsvmNeuResult.mat")$w;
rownames(beta) <- label
# top absolute coefficient values:
print("#############neutral class####################")
word =label[order(abs(beta),decreasing=T)][1:num];
coefficient = sort(abs(beta),decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top positive coefficient values:
word =label[order(beta,decreasing=T)][1:num];
coefficient = sort(beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top negative coefficient values:
word =label[order(-beta,decreasing=T)][1:num];
coefficient = sort(-beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);

# 4. L1Norm SVM word image for the neutral class:
# create the new tag vector: +1 for neutral class; -1 for all other classes
beta = readMat("./lpsvmSpamResult.mat")$w;
rownames(beta) <- label
# top absolute coefficient values:
print("#############spam class####################")
word =label[order(abs(beta),decreasing=T)][1:num];
coefficient = sort(abs(beta),decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top positive coefficient values:
word =label[order(beta,decreasing=T)][1:num];
coefficient = sort(beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
# top negative coefficient values:
word =label[order(-beta,decreasing=T)][1:num];
coefficient = sort(-beta,decreasing=T)[1:num];
temp = data.frame(word,coefficient);
print(temp);
