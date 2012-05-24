%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Framestart detektieren
% -----------------------------------------------------------------------------------------

function [SignalOut,OldData] = DetFrameStartStream2(Signal,Offset)

RSSI = zeros(1,length(Signal));                                         % Speicher für Werte der Moving Sum (Nur für Debug, kann weggekürzt werden)

ABS_Signal = abs(Signal);                                               % Betrag des komplexen Signals bilden

AddRange = 100;                                                         % Anzahl Werte für Moving Sum definieren
RSSI(AddRange) = sum(ABS_Signal(1:AddRange));                           % Moving Sum über die ersten Werte bilden

i=AddRange+1;
while i<length(Signal)-196608-Offset                                    % Datenstrom durchsuchen
    RSSI(i) = RSSI(i-1) + ABS_Signal(i) - ABS_Signal(i-AddRange);       % Moving Sum
    
    if (RSSI(i)/AddRange*8 < ABS_Signal(i))                             % Framestart suchen
         
         SignalOut = Signal(i+Offset:i+76*2552+Offset-1);               % Daten des detekterten DAB Frames (inkl. Offset)
         OldData = Signal(i+76*2552+Offset:end);                        % Noch nicht verwendete Daten
         return;

    end
    i=i+1;
end

% Kein Framestart detektiert
OldData = Signal;       % Alle Daten wiederverwenden (Wenn lange keine Detektion überlauf! Ev. Datengrösse begrenzen)
SignalOut = [];         % Keine DAB Framedaten, da kein Start detektiert wurde