%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Zeit in Samples zwischen zwei Frames (Frequenzstabilität)
% -----------------------------------------------------------------------------------------

function [] = FreqStab(FrameStartpoints)

x = FrameStartpoints(2:length(FrameStartpoints))-FrameStartpoints(1:length(FrameStartpoints)-1);
y= find(x>195000);
x = x(min(y):length(x));
figure('Name','Freq Histogramm');
hist(x-196608)