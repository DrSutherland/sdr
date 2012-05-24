%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% (De) Frequency interleaving  (Standard Page 157,158)
% -----------------------------------------------------------------------------------------

function [DeintFFTFrame] = FreqDeInterleaving(InterleavingTab,fft_Frame,FreqIntTabSize)

% Aus Interleaving-Tabelle die Deinterleavingtabelle erzeugen
DeinterleaverTab = sortrows(InterleavingTab(:,4:5),2);                  % Deinterleaver Tabelle auf Matlab Matrix schreibweise anpassen
DeinterleaverTab = DeinterleaverTab(FreqIntTabSize/4+1:end,:);          % Leerstellen entfernen
DeinterleaverTab(:,3) = [DeinterleaverTab(1:FreqIntTabSize/8*3,2)+1 ; DeinterleaverTab(FreqIntTabSize/8*3+1:FreqIntTabSize/8*6,2)]+FreqIntTabSize/8*3; % (k)Carrier aus Standard
DeinterleaverTab(:,4) = DeinterleaverTab(:,1)+1;                        % (n) Symbol aus Standard



DeintFFTFrame = zeros(size(fft_Frame));
for r=1:length(DeinterleaverTab(:,4))                                   % Frequenz Deinterleaving
    DeintFFTFrame(:,DeinterleaverTab(r,4)) = fft_Frame(:,r);
end