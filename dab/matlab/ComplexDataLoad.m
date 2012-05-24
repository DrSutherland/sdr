%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Stück des aufgezeichneten Files laden
% -----------------------------------------------------------------------------------------

function [Signal] = ComplexDataLoad (ReadFile,ReadSize,fs_file,fs)

t = fread (ReadFile, [2, ReadSize], 'float');
v = t(1,:) + t(2,:)*i;
[r, c] = size (v);
v = reshape (v, c, r);

Signal = resample(v, fs/1e3, fs_file/1e3);                    % Samplingrate anpassen (Standard Page 145, T = 1/2048000 s )
