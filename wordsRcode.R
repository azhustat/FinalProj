# STAT 215B, Spring 2012
# Final Project
# word counts

dat <- read.table("words.txt", header=FALSE)
dat <- dat[ order(dat[ , 2], decreasing=TRUE), ]
rownames(dat) <- 1:(dim(dat)[1])
names(dat) <- c("word", "counts")
dim(dat) # 7776    2
summary(dat$counts)
head(dat, 20)

# examines the words with frequency >= 10
sum(dat$counts >= 10) # 756
mat <- subset(dat, counts >= 10)
dim(mat) # 756 2
# write.table(mat$word, file="selectedwords.txt", row.names=FALSE, col.names=FALSE, fileEncoding="UTF-8", quote=FALSE)


# examines the co-occurrence  matrix
coocmat <- data.matrix(read.table("coocmat.txt", header=FALSE))
dim(coocmat) # 756 756
sum(coocmat - t(coocmat)) # 0, matrix is symmetric
coocmat[1:10, 1:10]

wordLabel = read.table("selectedwords.txt");

coocmat = matrix(0,795,795)
for (i in 1:3000){
  occurIndex = which(freqmat[,i]>0)
  if (length(occurIndex)>=2){ 
  edges = combn(occurIndex,2)
  for (j in 1:dim(edges)[2]){
    edge = edges[,j]
    coocmat[edge[1],edge[2]] = coocmat[edge[1],edge[2]] + 1
    coocmat[edge[2],edge[1]] = coocmat[edge[1],edge[2]]
  }
  }
}
rownames(coocmat) <- wordLabel$V1
colnames(coocmat) <- wordLabel$V1

# plot the matrix
matrixPlot(coocmat[1:50,1:50],zlim=c(0,100))

# now plot the occurence network
library(igraph)
n = 50 # top 30 mostly used words
s = coocmat[1:n,1:n];
s[s<10] = 0
wordCoGraph <- graph.adjacency(s, weighted=T,mode="undirected")
w = E(wordCoGraph)$weight
set.seed(215)
l <- layout.fruchterman.reingold(guassianGraph)
plot(wordCoGraph, 
     layout=l,#ayout.fruchterman.reingold(wordCoGraph), 
     vertex.label=wordLabel$V1[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)),
      edge.color = "red", 
     edge.width=abs(w)*0.01, vertex.size=8, 
     vertex.label.cex=.7, vertex.label.color="black")



tkplot(wordCoGraph, 
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

=======
# examines the frequency matrix
freqmat <- data.matrix(read.table("freqmat.txt", header=FALSE))
dim(freqmat) # 756 3000
summary(rowSums(freqmat))
rownames(freqmat) <- wordLabel$V1
matrixPlot(freqmat[1:50,1:50]);
# singular value decompositoin
svdresult = svd(freqmat)

library(elasticnet)
deleteWordIndex = -c(2,3,4,9,12,18,19);
seleWord = (1:100)[deleteWordIndex]  
out1<-spca(t(freqmat[seleWord,]),K=4,type="predictor",
           sparse="penalty",trace=TRUE,para=c(1,1,1,1))
sort(abs(out1$loadings[,1]),decreasing=T)[1:20]
sort(abs(out1$loadings[,2]),decreasing=T)[1:20]
sort(abs(out1$loadings[,3]),decreasing=T)[1:10]
sort(abs(out1$loadings[,4]),decreasing=T)[1:10]

# LASSO and SVM
library(glasso)
# GLasso: Gaussian Graphical Model
S = cov(t(freqmat));
graphPlot(S,50,lambda_max=0.03,lambda_min=0.01,
          numPlots=10,weighted = TRUE,vertex.size = 8,layout=l)
matrixPlot(S[1:50,1:50],zlim=c(-.04,.04))
gLassoResult = glasso(S,.02);
G = gLassoResult$wi
G2 = G - diag(diag(G));
G1 = (G2+t(G2))/2
# first of all, a matrix image plot
matrixPlot(G2[1:50,1:50],zlim=c(-4,4))
n = 50 # top 50 mostly used words
guassianGraph <- graph.adjacency(G1[1:n,1:n], weighted=T,mode="undirected")
w = E(guassianGraph)$weight

edgeColor = rep("red",length(w));
edgeColor[w>0] = "black"

w[abs(w)>2] =2
set.seed(215)
l <- layout.fruchterman.reingold(guassianGraph)
plot(guassianGraph, 
     layout=l, 
     vertex.label=wordLabel$V1[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)),
      edge.color = edgeColor, 
     edge.width=abs(w)*5,, vertex.size=10, 
     vertex.label.cex=.7, vertex.label.color="black")
tkplot(guassianGraph, 
     layout=layout.circle, 
     vertex.label=colnames(coocmat)[1:n],     
     #vertex.color=c(rep("red",4),rep("blue",6)),
      edge.color = edgeColor, 
     edge.width=abs(w)*100, vertex.size=15, 
     vertex.label.cex=1, vertex.label.color="black")

# LASSO 
tags = read.table("sampletags.txt")$V1
# 1. LASSO word image for the positive class:
# create the new tag vector: +1 for positive class; -1 for all other classes
y = tags;
y[y==0] = -1;
y[y==9] = -1;
library(lars)       
lassoPathResultPos = lars(t(freqmat),y);
# How do we choose lambda the regularization parameter? do a
# 10-fold cross validation...
# takes minutes to run...
cvPos = cv.lars(t(freqmat),y);
      bestFrac = cvPos$index[which(cvPos$cv==min(cvPos$cv))];
      betaL1Norm = rowSums(abs(lassoPathResultPos$beta))
      betaL1Frac = betaL1Norm/max(betaL1Norm)
      bestIndex = which(betaL1Frac>bestFrac)[1]
cvPlot(cvPos)
# runs like 30 sec; real fast
# the path plot; dont run it, real slow...
<<<<<<< HEAD
#plot(lassoPathResultPos,breaks=F)
# the beta matrix, of size 876*795; each row for a lambda value
=======
plot(lassoPathResultPos,breaks=F)
# the beta matrix, of size 876*756; each row for a lambda value
>>>>>>> 5e4219b10d526503441f4a3c39249117e88dc7ef
dim(lassoPathResultPos$beta);
beta = lassoPathResultPos$beta[bestIndex,] 
       # just pick the best lambda with the lowest cv error
print("#############positive#################")
# top absolute coefficient values:
sort(abs(beta),decreasing=T)[1:20]
# top positive coefficient values:
sort(beta,decreasing=T)[1:20]
# top negative coefficient values:
sort(-beta,decreasing=T)[1:20]
       
# 2. LASSO word image for the negative class:
# create the new tag vector: +1 for negative class; -1 for all other classes
y = tags;
y[tags==-1] = 1;
y[tags==0 | tags ==1|tags==9] = -1;
lassoPathResultNeg = lars(t(freqmat),y)
# the path plot; dont run it, real slow...
plot(lassoPathResultNeg,breaks=F)
<<<<<<< HEAD
cvNeg = cv.lars(t(freqmat),y);
      betaL1Norm = rowSums(abs(lassoPathResultNeg$beta))
      bestFrac = cvNeg$index[which(cvNeg$cv==min(cvNeg$cv))];
      betaL1Frac = betaL1Norm/max(betaL1Norm)
      bestIndex = which(betaL1Frac>bestFrac)[1]
cvPlot(cvNeg)
# the beta matrix, of size 846*795; each row for a lambda value
=======
# the beta matrix, of size 846*756; each row for a lambda value
>>>>>>> 5e4219b10d526503441f4a3c39249117e88dc7ef
dim(lassoPathResultNeg$beta);
beta = lassoPathResultNeg$beta[bestIndex,] # just pick one lambda
hist(beta)
print("###########negative################")
# top absolute coefficient values:
sort(abs(beta),decreasing=T)[1:20]
# top positive coefficient values:
sort(beta,decreasing=T)[1:20]
# top negative coefficient values:
sort(-beta,decreasing=T)[1:20] #warning: lots of zeros!

# 3. LASSO word image for the unidentifiable class:
# create the new tag vector: +1 for unidentifiable class; -1 for all other classes
y = tags;
y[tags==0] = 1;
y[tags==-1 | tags ==1|tags==9] = -1;
lassoPathResultNeu= lars(t(freqmat),y)
plot(lassoPathResultNeu,breaks=F)
<<<<<<< HEAD
cvNeu = cv.lars(t(freqmat),y);
      bestFrac = cvNeu$index[which(cvNeu$cv==min(cvNeu$cv))];
      betaL1Norm = rowSums(abs(lassoPathResultNeu$beta))
      betaL1Frac = betaL1Norm/max(betaL1Norm)
      bestIndex = which(betaL1Frac>bestFrac)[1]
cvPlot(cvNeu)
       # the beta matrix, of size 860*795; each row for a lambda value
=======
# the beta matrix, of size 860*756; each row for a lambda value
>>>>>>> 5e4219b10d526503441f4a3c39249117e88dc7ef
dim(lassoPathResultNeu$beta);
beta = lassoPathResultNeu$beta[bestIndex,] # just pick one lambda
hist(beta)
print("###############neutral###############")
# top absolute coefficient values:
sort(abs(beta),decreasing=T)[1:20]
# top positive coefficient values:
sort(beta,decreasing=T)[1:20]
# top negative coefficient values:
sort(-beta,decreasing=T)[1:20]

# 4. LASSO word image for the spam class:
# create the new tag vector: +1 for unidentifiable class; -1 for all other classes
y = tags;
y[tags==-9] = 1;
y[tags==-1 | tags ==1|tags==0] = -1;
lassoPathResultSpam= lars(t(freqmat),y)
# the path plot; dont run it, real slow...
plot(lassoPathResultSpam,breaks=F)
<<<<<<< HEAD
cvSpam = cv.lars(t(freqmat),y);
      bestFrac = cvSpam$index[which(cvSpam$cv==min(cvSpam$cv))];
      betaL1Norm = rowSums(abs(lassoPathResultSpam$beta))
      betaL1Frac = betaL1Norm/max(betaL1Norm)
      bestIndex = which(betaL1Frac>bestFrac)[1]
cvPlot(cvSpam)
# the beta matrix, of size 836*795; each row for a lambda value
=======
# the beta matrix, of size 836*756; each row for a lambda value
>>>>>>> 5e4219b10d526503441f4a3c39249117e88dc7ef
dim(lassoPathResultSpam$beta);
beta = lassoPathResultSpam$beta[bestIndex,] # just pick one lambda
hist(beta)
print("################spam##################")
# top absolute coefficient values:
sort(abs(beta),decreasing=T)[1:20]
# top positive coefficient values:
sort(beta,decreasing=T)[1:20]
# top negative coefficient values:
sort(-beta,decreasing=T)[1:20]

#
library(lpRegPath)
l1svmCVPos = risk.svm.L1(y, t(freqmat), intercept=TRUE, 
                          fold=4, repetition=2)

l1svmPos = fit.svm.L1(y, t(freqmat), intercept=TRUE, fold=4, repetition=2)

