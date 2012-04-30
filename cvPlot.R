cvPlot <- function(cvObj){
  ylim = c(min(cvObj$cv - cvObj$cv.error),max(cvObj$cv+cvObj$cv.error))
  plot(cvObj$index,cvObj$cv,type = "o",xlab ="l1 norm fraction",
       ylab="cross validation error",ylim = ylim);
  points(cvObj$index,cvObj$cv + cvObj$cv.error,type="o",col="red");
  points(cvObj$index,cvObj$cv - cvObj$cv.error,type="o",col="red");  
}