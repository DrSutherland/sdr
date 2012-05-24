%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Time interleaving
% -----------------------------------------------------------------------------------------
function [TiIntSubChDataOut, DataNextRound] = TimeInterleavingStream(NewSubChData,SubChSize,DataLastRound)

NewTiIntSubChData=reshape(NewSubChData',16,[]);                                     % Neue Daten

InhaltSize = length(NewSubChData(:,1));                                             % Anzahl erhaltene CIF

DelayCIF = SubChSize*64/16;                                                         % Verzögerung ein CIF
                                                         
DataLastRound(1, 1+DelayCIF*15:DelayCIF*(15+InhaltSize)) = NewTiIntSubChData(1,:);  % Bit1, 15 CIF verzögert
DataLastRound(2, 1+DelayCIF*7 :DelayCIF*(7+InhaltSize))  = NewTiIntSubChData(2,:);  % Bit2, 7 CIF verzögert
DataLastRound(3, 1+DelayCIF*11:DelayCIF*(11+InhaltSize)) = NewTiIntSubChData(3,:);  % Bit3, 11 CIF verzögert
DataLastRound(4, 1+DelayCIF*3 :DelayCIF*(3+InhaltSize))  = NewTiIntSubChData(4,:);  % Bit4, 3 CIF verzögert
DataLastRound(5, 1+DelayCIF*13:DelayCIF*(13+InhaltSize)) = NewTiIntSubChData(5,:);  % Bit5, 13 CIF verzögert
DataLastRound(6, 1+DelayCIF*5 :DelayCIF*(5+InhaltSize))  = NewTiIntSubChData(6,:);  % Bit6, 5 CIF verzögert
DataLastRound(7, 1+DelayCIF*9 :DelayCIF*(9+InhaltSize))  = NewTiIntSubChData(7,:);  % Bit7, 9 CIF verzögert
DataLastRound(8, 1+DelayCIF*1 :DelayCIF*(1+InhaltSize))  = NewTiIntSubChData(8,:);  % Bit8, 1 CIF verzögert
DataLastRound(9, 1+DelayCIF*14:DelayCIF*(14+InhaltSize)) = NewTiIntSubChData(9,:);  % Bit9, 14 CIF verzögert
DataLastRound(10,1+DelayCIF*6 :DelayCIF*(6+InhaltSize))  = NewTiIntSubChData(10,:); % Bit10 ,6 CIF verzögert
DataLastRound(11,1+DelayCIF*10:DelayCIF*(10+InhaltSize)) = NewTiIntSubChData(11,:); % Bit11 ,10 CIF verzögert
DataLastRound(12,1+DelayCIF*2 :DelayCIF*(2+InhaltSize))  = NewTiIntSubChData(12,:); % Bit12 ,2 CIF verzögert
DataLastRound(13,1+DelayCIF*12:DelayCIF*(12+InhaltSize)) = NewTiIntSubChData(13,:); % Bit13 ,12 CIF verzögert
DataLastRound(14,1+DelayCIF*4 :DelayCIF*(4+InhaltSize))  = NewTiIntSubChData(14,:); % Bit14 ,4 CIF verzögert
DataLastRound(15,1+DelayCIF*8 :DelayCIF*(8+InhaltSize))  = NewTiIntSubChData(15,:); % Bit15 ,8 CIF verzögert
DataLastRound(16,1+DelayCIF*0 :DelayCIF*(0+InhaltSize))  = NewTiIntSubChData(16,:); % Bit16 ,0 CIF verzögert

DataNextRound = circshift(DataLastRound, [0 -4*DelayCIF]);                          % Rotieren um vier CIF (da in Mode 1 ein DAB Frame = 4 CIFs)

TiIntSubChDataOut = reshape(DataLastRound(1:4*SubChSize*64),[],4)';                 % Interleavte Daten