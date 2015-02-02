function [BestRef,BestRefVar,cN]=getBestRefPic_q(Pic,REF)
% getBestRefPic calculates the best reference picture for the atom picture 
% 'Pic' from the reference picture set REF by LU decomposed B matrix
% for reference look in PRA 82 061606
% Version 30/10/2014

ind=find(REF.LogicBg);
A=double(Pic(ind)); % calculate intensity on pic 
    
meanRef=mean(REF.R,2);
V=REF.R(:,ind)*A;

lower.LT=true;
upper.UT=true;
c=linsolve(REF.U,linsolve(REF.L,V(REF.p,:),lower),upper);
BestRef=zeros(size(REF.refimgs{1}));
BestRefVar=zeros(size(REF.refimgs{1}));

% add up best refpic;

cN=c.*meanRef;

BestRef=reshape(REF.R'*c,size(Pic));
BestRefVar=reshape(REF.R'*(c.^2),size(Pic));



