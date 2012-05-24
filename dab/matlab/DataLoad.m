%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Aufgezeichnete Files Laden
% -----------------------------------------------------------------------------------------

function [Signal] = DataLoad(Filename, AnzSample)

b=read_complex_binary(Filename,AnzSample);              % Record1 -> 2 MSample, 9.8Sec, 20 091 724 Samples, 227.360MHz
                                                        % Record2 -> 2 MSample, 10.2Sec, 20 314 354 Samples, 194.064MHz

fs_file = 2e6;
fs = 2.048e6;

b = resample(b, fs/1e3, fs_file/1e3);                   % Resampling 2MS -> 2.048MS, Standard Page 145, T = 1/2048000 s

Signal = b;