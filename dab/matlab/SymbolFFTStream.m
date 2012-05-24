%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% FFT von allen Symbolen
% -----------------------------------------------------------------------------------------

function [fft_Array2] = SymbolFFTStream(Data,SymbolAnz,CarrierAnz,DurSymbol,N)

fft_Array = zeros([SymbolAnz-3,CarrierAnz]);    % DAB Frame FFT Array vorbereiten

for Frame = 3:SymbolAnz-1                       % Für den MSC werden nur die Symbole 3-76 gebraucht
    i=Frame*DurSymbol;                          % In den Daten die Symbole herausbilden
    Symbol = Data(i+1:i+N);                     % Daten eines OFDM Symbols herauslesen

    Y = fft(Symbol);                            % FFT des OFDM Symbols bilden
    Y = fftshift(Y);                            % FFT drehen, damit negativer Frequenzbereich am richtigen Ort steht

    fft_Array(Frame+1-3,(1:CarrierAnz/2))=Y(N/2-CarrierAnz/2+1:N/2);                % FFT in DAB Frame FFT Array schreiben (Aufgeteilt, da auf....
    fft_Array(Frame+1-3,(CarrierAnz/2+1:CarrierAnz))=Y(N/2+2:N/2+CarrierAnz/2+1);   % .... Zenterfrequenz kein Signal ist)
end

fft_Array2 = fft_Array(2:SymbolAnz-3,:) .* conj(fft_Array(1:SymbolAnz-1-3,:));    % Differenz zum vorherigen Symbol berechnen