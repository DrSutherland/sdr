%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Mode Bestimmung
% -----------------------------------------------------------------------------------------

function [SymbolAnz,Mode,N,DurSymbol,CarrierAnz,Offset,FreqIntTabSize] = DetMode(FrameStartpoints)

Samples = FrameStartpoints(2)-FrameStartpoints(1); %Transmission Frame Duration

SymbolAnz = 76;

if (Samples > 147456)              % Mode 1
    Mode = 1;
    N = 2^11;
    DurSymbol = 2552;
    CarrierAnz = 1536;
    
    Offset = 100;                   % 100 = Sehr gut, 0 = Fast zufrüh, über 500 schlecht (siehe Guard Time)
    FreqIntTabSize = 2048;
    
    
elseif (Samples > 73728)            % Mode 4
    Mode = 4;
    N = 2^10;
    DurSymbol = 1276;
    CarrierAnz = 768;
    Offset = 50;
    FreqIntTabSize = 1023;
    
end