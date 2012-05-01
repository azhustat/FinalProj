freqmat = dlmread('./freqmat.txt')';
tags = dlmread('./sampletags.txt');
cases = [1,-1,0,9];
for i = 1:4
whichCase = cases(i)
if whichCase == 1
  y = tags;
  y(find(y==0)) = -1;
  y(find(y==9)) = -1;
end
if whichCase == -1
  y = tags;
  y(find(tags==-1)) = 1;
  y(find(tags==0 | tags ==1|tags==9)) = -1;
end
if whichCase == 0
  y = tags;
  y(find(tags==0)) = 1;
  y(find(tags==-1 | tags ==1|tags==9)) = -1;
end
if whichCase == 9
  y = tags;
  y(find(tags==9)) = 1;
  y(find(tags==-1 | tags ==1|tags==0)) = -1;
end

%nu = 0.00

[w, gamma,trainCorr,testCorr,time,nu]=lpsvm(freqmat,y,10,0,1,10e-3);
if whichCase == 1
  save('lpsvmPosResult.mat','w','gamma','trainCorr','testCorr','nu');
end
if whichCase == -1
  save('lpsvmNegResult.mat','w','gamma','trainCorr','testCorr','nu');
end
if whichCase == 0
  save('lpsvmNeuResult.mat','w','gamma','trainCorr','testCorr','nu');
end
if whichCase == 9
  save('lpsvmSpamResult.mat','w','gamma','trainCorr','testCorr','nu');
end

end
%lpsvm(A,d,k,nu,output,delta)
