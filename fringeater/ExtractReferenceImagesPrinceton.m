function [refs,Bjk,L,U,p,R]=ExtractReferenceImagesPrinceton_q(FileName,LogicBg)
% Version 30/10/2014

ImagingParameters;
Path=todayPath;
ImageType='tif';


separator = '/';

if isempty(FileName) 
    
    imageNames=uipickfiles('FilterSpec',[Path '*.' ImageType],'out','cell');
else
    if  ischar(FileName)
        imageNames={FileName};
    else
        imageNames=FileName;
    end
end

counter=1,
R=[];
refs=[];
for C1=1:length(imageNames)
    disp(['Load reference image: ' num2str(C1) '/' num2str(length(imageNames))])
    data=imread(char(imageNames{C1}),ImageType);
    pic2=data(Pic2Start:Pic2End,:);
    
    if mean(mean(pic2(LogicBg)))>CCDOffset+300;
        refs{counter}=pic2-CCDOffset;
        R(counter,:)=double((refs{counter}(:)));
        counter=counter+1;
    else
        disp([imageNames{C1} ' seems to have almost no intensity and is not used!!'])
    end
end
ind=find(LogicBg);
disp(['Creating Bjk']);
Bjk=R(:,ind)*R(:,ind)';
disp(['LU decompose Bjk']);
[L,U,p]=lu(Bjk,'vector');