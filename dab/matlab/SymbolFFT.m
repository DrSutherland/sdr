%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% FFT von allen Symbolen bilden
% -----------------------------------------------------------------------------------------

function [fft_Array2] = SymbolFFT(Data,FrameNr,FrameStartpoints,SymbolAnz,CarrierAnz,DurSymbol,Offset,N,PlotOn)

fft_Array = zeros([SymbolAnz,CarrierAnz]);

for Frame = 0:SymbolAnz-1
    i=Frame*DurSymbol;
    Symbol = Data(FrameStartpoints(FrameNr)+i+Offset:FrameStartpoints(FrameNr)+N-1+i+Offset);

    Y = fft(Symbol);                                                                    % FFT bilden und drehen
    Y = fftshift(Y);

    fft_Array(Frame+1,(1:CarrierAnz/2))=Y(N/2-CarrierAnz/2+1:N/2);                      % Leerer Zentercarrier entfernen
    fft_Array(Frame+1,(CarrierAnz/2+1:CarrierAnz))=Y(N/2+2:N/2+CarrierAnz/2+1);
end

fft_Array2 = fft_Array(2:SymbolAnz,:) .* conj(fft_Array(1:SymbolAnz-1,:));              % Differenz zum vorherigen Symbol berechnen

if PlotOn == 1
    figure('Name','Phasenverlauf');
    plot(angle(fft_Array2(:,:)),'*');              % Phasenverlauf über alle Carrier
    figure('Name','Augendiagramm');
    plot(angle(fft_Array2(:,:)));                  % Augendiagramm über alle Carrier
    xlim([1,10])
    figure('Name','Punktwolke QAM');
    plot(fft_Array2(:,805),'*');                  % Polarplot eines QAM Carriers als Punktwolke
    axis equal;
    grid;
end