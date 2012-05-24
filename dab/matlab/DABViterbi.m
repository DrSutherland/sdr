%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Viterbi Decoder
% -----------------------------------------------------------------------------------------

function [BitDef] = DABViterbi(yIn)

Generator = [1 0 1 1 0 1 1;...                                               % Faltungsencoder
             1 1 1 1 0 0 1;...
             1 1 0 0 1 0 1;...
             1 0 1 1 0 1 1];
         
lange = length(Generator(:,1));

y=reshape(yIn,lange,length(yIn)/lange)';

SpeicherTabs = length(Generator(1,:)) - 1;
MemDeep= 5*SpeicherTabs;                                                                % Speichertiefe für Symbolentscheid (Faustregel)
y=[y;zeros(MemDeep,lange)];

Pfad = mod ([(0:2^SpeicherTabs-1)'*2 (0:2^SpeicherTabs-1)'*2+1],2^SpeicherTabs);        % Welche Zustände miteinander verbunden sind
                                                                                        % Bsp: Zustan 10 = Index 2 = Moegliche Herkunftsindex 0 oder 1

Pfadspeicher = zeros(2^SpeicherTabs,MemDeep);                                           % Speichert die Siegerpfade
Metrik = -1000*ones(2^SpeicherTabs,2);                                                  % Metrik der letzten beiden Symbole
Metrik(1) = 0;                                                                          % Metrikstart auf null setzen
BitDef = zeros(1,length(y(:,1))-MemDeep);                                               % Codewort
BitIndex = 1;                                                                           % Zeiger auf neustes Codewort

for i=1:length(y(:,1))                                                                  % Symbol
    for index=1:2^SpeicherTabs                                                          % Level
        
        if index > 2^(SpeicherTabs-1)
            NewBit = 1;
            StepOutGen1=[NewBit double(dec2bin(Pfad(index,1),SpeicherTabs)-'0')];       % Annahme Ursprung Pfad 1: Bits des Codeworts (neues Bit und Speichertabs)
            StepOutGen2=[NewBit double(dec2bin(Pfad(index,2),SpeicherTabs)-'0')];       % Annahme Ursprung Pfad 2: Bits des Codeworts (neues Bit und Speichertabs)
        else 
            NewBit = 0;
            StepOutGen1=[NewBit double(dec2bin(Pfad(index,1),SpeicherTabs)-'0')];       % Annahme Ursprung Pfad 1: Bits des Codeworts (neues Bit und Speichertabs)
            StepOutGen2=[NewBit double(dec2bin(Pfad(index,2),SpeicherTabs)-'0')];       % Annahme Ursprung Pfad 2: Bits des Codeworts (neues Bit und Speichertabs)
        end
        Ref1 = 1-2.*mod(StepOutGen1*Generator',2);                    % Optimales Empfangsergebnis zwischen zwei MetrikTabs
        Value1 = Ref1 * y(i,:)'+Metrik(Pfad(index,1)+1,1);            % Resultierende Metrikveränderung bei verwenden des Übergangs 1
        Ref2 = 1-2.*mod(StepOutGen2*Generator',2);                    % Optimales Empfangsergebnis zwischen zwei MetrikTabs
        Value2 = Ref2 * y(i,:)'+Metrik(Pfad(index,2)+1,1);            % Resultierende Metrikveränderung bei verwenden des Übergangs 2
        
        if Value1 > Value2                                            % Entscheiden welcher Pfad besser war
            Metrik(index,2) = Value1;                                 % Metrik anpassen
            Pfadspeicher(index,end) = Pfad(index,1);                  % Pfad abspeichern
        else
            Metrik(index,2) = Value2;                                 % Metrik anpassen
            Pfadspeicher(index,end) = Pfad(index,2);                  % Pfad abspeichern
        end
    end
    if i > MemDeep                                                    % Nach einigen Symolen mit dem bestimmen der Daten beginnen
        [Nothing, Pos] = max(Metrik(:,2));                                  % Maximaler Wert an der Metrikspitze suchen
        for p=0:MemDeep-1                                             % Weg zurückverfolgen
            Pos=Pfadspeicher(Pos,end-p)+1;
        end
        Pos = Pos - 1;
        if Pos >=2^(SpeicherTabs-1)                                   % Aus dem Ende der Weg zurückverfolgung das Bit bestimmen
            BitDef(BitIndex) = 1;
        else
            BitDef(BitIndex) = 0;
        end
        BitIndex = BitIndex +1;                                       % Bit Index erneuern
    end
    Pfadspeicher = circshift(Pfadspeicher,[0 -1]);                    % Ringspeicher für den nächsten durchlauf vorbereiten
    Metrik = circshift(Metrik,[0 -1]);
end