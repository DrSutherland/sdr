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

function [FrameStartpoints] = DetFrameStart(Signal,PlotOn)

TOC_Old = toc;

forgett_Signal = 3;                                                 % Vergessensfaktor für Signal Moving Average Filter

Signal_Pegel = zeros(1,length(Signal));
FrameStartpoints = zeros(1,1000);
Delay = 2^6;
Pause = 2^13;

ABS_Signal = abs(Signal);
 
for i=1:length(Signal)-1
     Signal_Pegel(i+1) = Signal_Pegel(i) - Signal_Pegel(i)/(2^forgett_Signal) + ABS_Signal(i);        % Moving Average Filter
end
 
if PlotOn == 1                                                              % Plot RSSI und Signalamplitude
    figure('Name','Signal - RSSI');
    plot(1:length(Signal),ABS_Signal,...
         1+Delay:length(Signal)+Delay,Signal_Pegel);
    legend('Signal','RSSI')

    hold on;
end

fprintf('RSSI berechnen %3i Sek \n',round(toc-TOC_Old));
TOC_Old = toc;
 
index = 0;
for i=1+Delay:1:length(Signal)-1
    if (index < i)                                                          % Pause der Detektion
         if (Signal_Pegel(i-Delay) < ABS_Signal(i))                         % Framestart suchen

             if PlotOn == 1
                plot(i,ABS_Signal(i),'*','color','r');                      % Detektion markieren
             end

             FrameStartpoints(1) = i;                                       % Speichern der Position
             FrameStartpoints = circshift(FrameStartpoints,[0 -1]);

             index=i+Pause;                                                 % Ende der Detektionspause -> Indexposition (Verhindern von Doppeldetektion)
         end
    end
end

fprintf('Framestart berechnen %3i Sek \n',round(toc-TOC_Old));

y= find(FrameStartpoints>1000);
FrameStartpoints = FrameStartpoints(min(y):length(FrameStartpoints));       % Startpunkte der einzelnen Frames


if PlotOn == 1
    hold off;
end
