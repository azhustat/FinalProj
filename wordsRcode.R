# STAT 215B, Spring 2012
# Final Project
# word counts

dat <- read.table("words.txt", header=FALSE)
dat <- dat[ order(dat[ , 2], decreasing=TRUE), ]
rownames(dat) <- 1:(dim(dat)[1])
names(dat) <- c("word", "counts")
dim(dat) # 4370    2
summary(dat$counts)
head(dat, 20)