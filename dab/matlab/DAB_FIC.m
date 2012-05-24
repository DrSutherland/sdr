%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;clear all;close all;

tic;

% -----------------------------------------------------------------------------------------
% Aufgezeichnete Files Laden
% -----------------------------------------------------------------------------------------

[Signal] = DataLoad('../Aufzeichnungen/Record1.dat',2^20);                % Record1 -> 2 MSample, 9.8Sec, 20 091 724 Samples, 227.360MHz
                                                        % Record2 -> 2 MSample, 10.2Sec, 20 314 354 Samples, 194.064MHz

% -----------------------------------------------------------------------------------------
% Framestart detektieren
% -----------------------------------------------------------------------------------------

FrameStartpoints = DetFrameStart(Signal,0);                 

% -----------------------------------------------------------------------------------------
% Zeit in Samples zwischen zwei Frames (Frequenzstabilität), optional
% -----------------------------------------------------------------------------------------

%FreqStab(FrameStartpoints)





for FrameNr = 1:length(FrameStartpoints)-1

% -----------------------------------------------------------------------------------------
% Mode Bestimmung
% -----------------------------------------------------------------------------------------

[SymbolAnz,Mode,N,DurSymbol,CarrierAnz,Offset,FreqIntTabSize] = DetMode(FrameStartpoints);


% -----------------------------------------------------------------------------------------
% FFT von Symbol (1), optional
% -----------------------------------------------------------------------------------------

%fftSymb1(Signal,FrameStartpoints,N,fs);

% -----------------------------------------------------------------------------------------
% FFT von allen Symbolen
% -----------------------------------------------------------------------------------------

fft_Frame = SymbolFFT(Signal,FrameNr,FrameStartpoints,SymbolAnz,CarrierAnz,DurSymbol,Offset,N,0);

% -----------------------------------------------------------------------------------------
% Frequency interleaving
% -----------------------------------------------------------------------------------------

[InterleavingTab] = FreqInterleavingTab(FreqIntTabSize);

[DeintFFTFrame] = FreqDeInterleaving(InterleavingTab,fft_Frame,FreqIntTabSize);


% -----------------------------------------------------------------------------------------
% Symbol demapper
% -----------------------------------------------------------------------------------------

Data = zeros(1,(SymbolAnz-1)*CarrierAnz*2);                      % 76 FFT's -1 da differentiell

for f=1:SymbolAnz-2
    Data(1+(f-1)*CarrierAnz*2:(f)*CarrierAnz*2) = [real(DeintFFTFrame(f,:)) imag(DeintFFTFrame(f,:))];
end

% -----------------------------------------------------------------------------------------
% Aus den 3 FIC Symbole, die 4 Convolutional codewords bilden
% -----------------------------------------------------------------------------------------

FIC = zeros(4, 2*1536*3/4);

for r=0:3
    FIC(r+1,:) = Data(r*2304+1:(r+1)*2304);
end

% -----------------------------------------------------------------------------------------
% (De)puncturing (FIC)
% -----------------------------------------------------------------------------------------

DataDep = [depuncturing(FIC(:,1:2016),16) depuncturing(FIC(:,2017:2292),15) depuncturing(FIC(:,2293:2304),8)];

% -----------------------------------------------------------------------------------------
% Viterbi Decoder
% -----------------------------------------------------------------------------------------

DataVit = zeros(4,768+6);                   % Bitvektor + Tail

for f=1:4
DataVit(f,:) = DABViterbi(DataDep(f,:));
end

DataVit = DataVit(:,1:end-6);      % Tail wegnehmen

% -----------------------------------------------------------------------------------------
% Energy dispersal
% -----------------------------------------------------------------------------------------

DataEne = zeros(size(DataVit));
for m=1:4
DataEne(m,:) = xor(DataVit(m,:),EnergyDispGen(768));
end

% -----------------------------------------------------------------------------------------
% Bilden der FIB's
% -----------------------------------------------------------------------------------------

FIB=reshape(DataEne',256,12)';

% -----------------------------------------------------------------------------------------
% CRC16 Check der FIB's
% -----------------------------------------------------------------------------------------

FIBCRCCheck = [CRC16(FIB(1,:)) CRC16(FIB(2,:)) CRC16(FIB(3,:)) CRC16(FIB(4,:)) ...
               CRC16(FIB(5,:)) CRC16(FIB(6,:)) CRC16(FIB(7,:)) CRC16(FIB(8,:)) ...
               CRC16(FIB(9,:)) CRC16(FIB(10,:)) CRC16(FIB(11,:)) CRC16(FIB(12,:))];
           
if sum(FIBCRCCheck) ==12
   %disp('CRC OK');
else
   disp(['CRC Fail! Frame: ',num2str(FrameNr)]);
end

% -----------------------------------------------------------------------------------------
% FIG's aus FIB's bestimmen
% -----------------------------------------------------------------------------------------

for FIBNr=1:12
    pos = 1;
    while pos < 241
        
        if FIB(FIBNr,pos:pos+7) == [1 1 1 1 1 1 1 1], break,end
        
        % FIG Type und Länge aus FIB herauslesen
        Type = BintoDez(FIB(FIBNr,pos:pos+2),3);
        FIGDataLength = BintoDez(FIB(FIBNr,pos+3:pos+7),5);
        
        % FIG verarbeiten
        FIGType(FrameNr,FIBNr,Type,FIGDataLength,FIB(FIBNr,pos+8:pos+8*(FIGDataLength+1)-1))
        
        pos = pos + (FIGDataLength+1)*8;
    end
end

end



