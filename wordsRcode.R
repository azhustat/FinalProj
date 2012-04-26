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

wordLabel = read.table("selectedwords.txt");
rownames(coocmat) <- wordLabel$V1
colnames(coocmat) <- wordLabel$V1

# plot the matrix
matrixPlot(coocmat[1:20,1:20],zlim=c(0,100))

# now plot the occurence network
library(igraph)
n = 50 # top 30 mostly used words
s = coocmat[1:n,1:n];
s[s<10] = 0
wordCoGraph <- graph.adjacency(s, weighted=T,mode="undirected")
w = E(wordCoGraph)$weight

plot(wordCoGraph, 
     layout=layout.fruchterman.reingold,#layout.circle, 
     vertex.label=colnames(coocmat)[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)), 
     edge.width=E(wordCoGraph)$weight/50, vertex.size=15, 
     vertex.label.cex=1, vertex.label.color="black")


# check sampletags.txt
tags <- scan("sampletags.txt")
table(tags)
# -1    0    1    9 
#308 1323 1097  272 

# examines the conditional occurrence matrix
condmat <- data.matrix(read.table("condmat.txt", header=FALSE))
rownames(condmat) <- wordLabel$V1
colnames(condmat) <- c("negative","neutral","positive","spam")
dim(condmat) # 795 4
summary(rowSums(condmat))

<<<<<<< HEAD
cor(condmat) # approximately the same words appear in different categories

S = cov(t(condmat));
matrixPlot(S[1:50,1:50],zlim=c(0,5000))

library(R.matlab)
G = readMat("./GuassianGraphModel/words50l04.mat")$X;
# get rid of the diagonal entries
G2 = G - diag(diag(G));
# first of all, a matrix image plot
matrixPlot(G2[1:50,1:50],zlim=c(-.04,.04))
# divide into positve and negative relations:
Gp = matrix(0,nrow = dim(G2)[1],ncol=dim(G2)[2]);
Gp[G2>0] = G2[G2>0]
Gn = matrix(0,nrow = dim(G2)[1],ncol=dim(G2)[2]);
Gn[G2<0] = G2[G2<0]


n = 50 # top 50 mostly used words
guassianGraph <- graph.adjacency(Gn[1:n,1:n], weighted=T,mode="undirected")
w = E(guassianGraph)$weight

edgeColor = rep("red",length(w));
edgeColor[w>0] = "black"

plot(guassianGraph, 
     layout=layout.fruchterman.reingold, 
     vertex.label=colnames(coocmat)[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)),
      edge.color = edgeColor, 
     edge.width=abs(w)*100, vertex.size=15, 
     vertex.label.cex=1, vertex.label.color="black")
tkplot(guassianGraph, 
     layout=layout.circle, 
     vertex.label=colnames(coocmat)[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)),
      edge.color = edgeColor, 
     edge.width=abs(w)*100, vertex.size=15, 
     vertex.label.cex=1, vertex.label.color="black")
=======
# examines the frequency matrix
freqmat <- data.matrix(read.table("freqmat.txt", header=FALSE))
dim(freqmat) # 795 3000
summary(rowSums(freqmat))

>>>>>>> bcf00e32b9f85e75fefcdc7fe90f146875028fb6
