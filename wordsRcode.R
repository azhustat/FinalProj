# STAT 215B, Spring 2012
# Final Project
# word counts

dat <- read.table("words.txt", header=FALSE)
dat <- dat[ order(dat[ , 2], decreasing=TRUE), ]
rownames(dat) <- 1:(dim(dat)[1])
names(dat) <- c("word", "counts")
dim(dat) # 7862    2
summary(dat$counts)
head(dat, 20)

# examines the words with frequency >= 10
sum(dat$counts >= 10) # 795
mat <- subset(dat, counts >= 10)
dim(mat) # 795 2
# write.table(mat$word, file="selectedwords.txt", row.names=FALSE, col.names=FALSE, fileEncoding="UTF-8", quote=FALSE)


# examines the co-occurrence  matrix
coocmat <- data.matrix(read.table("coocmat.txt", header=FALSE))
dim(coocmat) # 795 795
sum(coocmat - t(coocmat)) # 0, matrix is symmetric
coocmat[1:10, 1:10]

# check sampletags.txt
tags <- scan("sampletags.txt")
table(tags)
# -1    0    1    9 
#308 1323 1097  272 

# examines the conditional occurrence matrix
condmat <- data.matrix(read.table("condmat.txt", header=FALSE))
dim(condmat) # 795 4
summary(rowSums(condmat))