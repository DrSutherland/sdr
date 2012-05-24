%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Berechnung der EEP Einstellungen (Standard Seite 135)
% -----------------------------------------------------------------------------------------
function [Audiokbps,PI1,PI2,L1Range,L2Range] = EEPTab (Protection,SubChSize)

if Protection(2) == 'A'             % EEP A Protection
    switch Protection(1)
        case '1'                    % Protectionlevel 1
            n = SubChSize/12;
            PI1 = 24;
            PI2 = 23;
            L1 = 6*n-3;
            L2 = 3;
            
        case '2'                    % Protectionlevel 2
            n = SubChSize/8;
            if n == 1
                PI1 = 13;
                PI2 = 12;
                L1 = 5;
                L2 = 1;
            else
                PI1 = 14;
                PI2 = 13;
                L1 = 2*n-3;
                L2 = 4*n+3;
            end
            
        case '3'                    % Protectionlevel 3
            n = SubChSize/6;
            PI1 = 8;
            PI2 = 7;
            L1 = 6*n-3;
            L2 = 3;
            
        case '4'                    % Protectionlevel 4
            n = SubChSize/4;
            PI1 = 3;
            PI2 = 2;
            L1 = 4*n-3;
            L2 = 2*n+3;
    end
    Audiokbps = n * 8;
else                                % EEP B Protection
   switch Protection(1)
        case '1'                    % Protectionlevel 1
            n = SubChSize/27;
            PI1 = 10;
            PI2 = 9;
        case '2'                    % Protectionlevel 2
            n = SubChSize/21;
            PI1 = 6;
            PI2 = 5;
        case '3'                    % Protectionlevel 3
            n = SubChSize/18;
            PI1 = 4;
            PI2 = 3;
        case '4'                    % Protectionlevel 4
            n = SubChSize/15;
            PI1 = 2;
            PI2 = 1;
   end
    Audiokbps = n * 32;
    L1 = 24*n-3;
    L2 = 3;
end

L1Range = L1*128*(PI1+8)/32;
L2Range = L2*128*(PI2+8)/32 + L1Range;