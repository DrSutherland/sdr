%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
%  Tabelle für Frequency interleaving erstellen (Standard Page 157,158)
% -----------------------------------------------------------------------------------------

function [InterleavingTab] = FreqInterleavingTab(FreqIntTabSize)

InterleavingTab = -1*ones(FreqIntTabSize,5);
InterleavingTab(1,1:2) = zeros(1,2);
InterleavingTab(1,5) = - FreqIntTabSize/2 -1;

InterleavingTab(:,1)=0:FreqIntTabSize-1;                                % Spalte 1 aus Standard erzeugen (i)
Zeile4Counter = 0;                                                      % Spalte 4 aus Standard vorbereiten
for m=2:FreqIntTabSize
    InterleavingTab(m,2) =  mod(13*InterleavingTab(m-1,2)+FreqIntTabSize/4-1,FreqIntTabSize);    % Spalte 2 aus Standard erzeugen (pi)
    
    if InterleavingTab(m,2) > FreqIntTabSize/8-1 && InterleavingTab(m,2) < FreqIntTabSize/8*7+1 && FreqIntTabSize/2 ~= InterleavingTab(m,2)
        InterleavingTab(m,3) = InterleavingTab(m,2);                    % Spalte 3 aus Standard erzeugen (dn)
        
        InterleavingTab(m,4) = Zeile4Counter;                           % Spalte 4 aus Standard erzeugen (n)
        Zeile4Counter = Zeile4Counter +1;
    end
    
    InterleavingTab(m,5) = InterleavingTab(m,3) - FreqIntTabSize/2;     % Spalte 5 aus Standard erzeugen (k)
end