cvPlot <- function(cvObj){
  ylim = c(min(cvObj$cv - cvObj$cv.error),max(cvObj$cv+cvObj$cv.error))
  plot(cvObj$index,cvObj$cv,type = "l",xlab ="l1 norm fraction",
       ylab="cross validation error",ylim = ylim);
  points(cvObj$index,cvObj$cv + cvObj$cv.error,type="l",col="red",lty=2);
  points(cvObj$index,cvObj$cv - cvObj$cv.error,type="l",col="red",lty=2);  
}