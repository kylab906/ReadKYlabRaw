% author: KYLAB S.L. Kuo ver.1 #8-bits convert
% author: KYLAB W.Y. Li  ver.2 #16-bits convert
function [Data, splr2, SRn] = ReadRAW

%讀取RAW檔
[filename,filepath]=uigetfile('*.RAW');
fileID = fopen([filepath filename]);
Raw=fread(fileID,'uint8');
fclose(fileID);

%Global Variable
header=Raw(1:512);
channel=[];
cont=ones(1,header(37));    %header(37) = Cnannel number
Data=zeros(1,header(37));
splr=string(char(header(40:54)));
start=55;%算SRn的頭
splr2=[];
splrtemp=[];
maxi=0;
%算sampling rate

for i=1:15
    splr2=strcat(splr2,splr(i,1));
end
splr2=str2double(splr2);

%抓取sampling rate 比值,最後存在SRn
SRn=zeros(1,header(37));
for i=1:header(37)
        SRtemp=string(char(header(start+1:start+1+15)));
        for j=1:15
          splrtemp=strcat(splrtemp,SRtemp(j,1));
        end
        splrtemp=str2double(splrtemp);
%         fprintf('%.1f\n',splrtemp);
        SRn(i)=splr2/splrtemp;
        if SRn(i)>maxi
            maxi=SRn(i);
        end
       start=start+1+15;
       splrtemp=[];
end
%建matrix
matrix=zeros(maxi,header(37));
for i=1:maxi
    for j=1:header(37)
        matrix(i,j)=i-1;
    end
end
%建channel
cnt=1;
for i=1:maxi
    for j=1:header(37)
        if mod(matrix(i,j),SRn(j))==0
             channel(cnt)=j;
             cnt=cnt+1;
        end
    end
end
Raw_Data = Raw(513:floor((length(Raw)-512)/(2*length(channel)))*(2*length(channel))+512);
for i=1:length(channel)*2:length(Raw_Data)
    for j=1:length(channel)
        Data(channel(j),cont(channel(j)))=Raw_Data(i+2*j-1)*256+Raw_Data(i+2*(j-1));
        cont(channel(j))=cont(channel(j))+1;
    end
end

% for k=1:header(37)
%     subplot(10,1,k);
%     plot(Data(k,:));
% end
