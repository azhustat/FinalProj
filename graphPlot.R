library(glasso)
library(igraph)
graphPlot <- function(S,n,lambda_max,lambda_min, vertex.size = 10, fontsize=0.8,
                      numPlots=5,weighted = TRUE){
  # S: convariance matrix
  # n: number of vertices to be displayed
  # lambda_max and lambda_min: max and min of lambda range
  # numPlots: number of plots to be produced
  lambda = seq(from = lambda_min, to = lambda_max, length.out = numPlots);
  
  gLassoResult = glasso(S, lambda_min);
  G = gLassoResult$wi
  G2 = G - diag(diag(G));
  G1 = (G2+t(G2))/2
  guassianGraph <- graph.adjacency(G1[1:n,1:n], weighted=weighted,
                                   mode="undirected")
  
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
      edge.width=abs(w)*5, vertex.size=vertex.size, 
      vertex.label.cex=fontsize, vertex.label.color="black")
  title("",xlab = paste(expression(lambda),"=",lambda_min))
  if (numPlots>1){ 
    for (i in 1:(numPlots-1)){
     gLassoResult = glasso(S, lambda[i+1]);
     G = gLassoResult$wi
     G2 = G - diag(diag(G));
     G1 = (G2+t(G2))/2
     guassianGraph <- graph.adjacency(G1[1:n,1:n], weighted=weighted,
                                   mode="undirected")
  
     w = E(guassianGraph)$weight

    edgeColor = rep("red",length(w));
    edgeColor[w>0] = "black"

    w[abs(w)>2] =2
    plot(guassianGraph, 
       layout=l, 
       vertex.label=wordLabel$V1[1:n],     
      #vertex.color=c(rep("red",4),rep("blue",6)),
        edge.color = edgeColor, 
        edge.width=abs(w)*5, vertex.size=vertex.size, 
        vertex.label.cex=fontsize, vertex.label.color="black")
     title("",xlab = paste("lambda","=",signif(lambda[i+1],4)))
    }
  }
}