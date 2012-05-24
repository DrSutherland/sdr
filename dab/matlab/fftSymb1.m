%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% FFT des ersten Symbols bilden und plotten
% -----------------------------------------------------------------------------------------

function [] = fftSymb1(Signal,FrameStartpoints,N,fs)

Symbol = Signal(FrameStartpoints(1):FrameStartpoints(1)+N-1);
figure('Name','Symbol1');
Y = abs(fft(Symbol));                       % FFT ausführen

Y = fftshift(Y);                            % FFT drehen
F = [-N/2:N/2-1]/N*fs;
plot(F,20*log10(Y));                        

[C I]=max(abs(Y));                          % Darstellung anpassen
freq=(I-1-N/2)*fs/length(Y);

ylim([20*log10(C)-50 20*log10(C)+1])
xlim([-N/2/N*fs (N/2-1)/N*fs])  