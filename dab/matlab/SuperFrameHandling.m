%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% -----------------------------------------------------------------------------------------
% Super Frame Handling (not finished)
% -----------------------------------------------------------------------------------------

function [DabFrameCount,SuperFrameSync,DataEneChain,au_start,num_aus] = SuperFrameHandling(DabFrameCount,SuperFrameSync,DataEneChain,au_start,Audiokbps,lan,num_aus)

DabFrameCount = DabFrameCount + 4;

while DabFrameCount >= 5

    if SuperFrameSync == true                                               % Superframe bereits synchronisiert?

        for r=1:num_aus-1
        au_start(r+1) = BintoDez(DataEneChain(25+12*(r-1):25+12*r-1),12);   % AU startadressen herauslesen
        end

        Audio = (reshape(DataEneChain',8,[])'*[128 64 32 16 8 4 2 1]')';    % Daten Bits zu Bytes umwandeln

        if lan == 1
            out.write(Audio(1:480),0,480);                                  % Netzwerkdatenstrom erzeugen
            out.flush();
        end

        for r=1:num_aus-1
            ModCoded = DataEneChain(au_start(r)*8+1:au_start(r+1)*8);       % AU Blöcke bilden
            if CRC16(ModCoded) == 1                                         % AU CRC prüfen
                disp('CRC OK')
            else
                SuperFrameSync = false;
                disp('CRC NOT')
            end
        end
        DataEneChain = circshift(DataEneChain,[0 -96*8*5]);                 % Datenkette nachführen
        DabFrameCount = DabFrameCount - 5;


    else                                                    % SuperFrame synchronisation suchen
        dac_rate = DataEneChain(18);
        sbr_flag = DataEneChain(19);

        switch BintoDez([dac_rate sbr_flag],2)              % Anzahl AU Startadressen herauslesen
            case 0
                num_aus = 4;
                au_start = zeros(1,num_aus+1);
                au_start(1) = 8; 
            case 1
                num_aus = 2;
                au_start = zeros(1,num_aus+1);
                au_start(1) = 5; 
            case 2
                num_aus = 6;
                au_start = zeros(1,num_aus+1);
                au_start(1) = 11; 
            case 3
                num_aus = 3;
                au_start = zeros(1,num_aus+1);
                au_start(1) = 6; 
        end
        au_start(num_aus+1) = Audiokbps/8*110;              % Adresse des letzten AU berechnen

        for r=1:num_aus-1                                   % Startadressen herauslesen
            au_start(r+1) = BintoDez(DataEneChain(25+12*(r-1):25+12*r-1),12);
        end

        if au_start(1) < au_start(2) && au_start(1)<Audiokbps/8*110 && au_start(2)<Audiokbps/8*110 % Synchronisation über CRC suchen
            ModCoded = DataEneChain(au_start(1)*8+1:au_start(2)*8);
            if CRC16(ModCoded) == 1
               SuperFrameSync = true;
            else
                DataEneChain = circshift(DataEneChain,[0 -96*8*1]);
                DabFrameCount = DabFrameCount - 1;
            end

        else
            DataEneChain = circshift(DataEneChain,[0 -96*8*1]);
            DabFrameCount = DabFrameCount - 1;
        end
    end
end  