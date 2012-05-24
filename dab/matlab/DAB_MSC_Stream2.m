%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Masterthesis
% Zürcher Hochschule für Angewandte Wissenschaften
% Zentrum für Signalverarbeitung und Nachrichtentechnik
% © Michael Höin
% 12.4.2011 ZSN
% info.zsn@zhaw.ch
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all;
close all;

import java.net.*
import java.io.*

% -----------------------------------------------------------------------------------------
% Senderauswahl
% -----------------------------------------------------------------------------------------

SubChStartAdr = 188;                  % DRS 3 (DAB)
SubChSize = 84;
Audiokbps = 128;
Protection = 4;
UEP = true;

% SubChStartAdr = 272;                  % DRS Musikwelle (DAB)
% SubChSize = 96;
% Audiokbps = 128;
% Protection = 3;
% UEP = true;

% SubChStartAdr = 368;                  % DRS Virus (DAB)
% SubChSize = 96;
% Audiokbps = 128;
% Protection = 3;
% UEP = true;

% SubChStartAdr = 548;                  % CH Classic (DAB)
% SubChSize = 84;
% Audiokbps = 128;
% Protection = 4;
% UEP = true;

% SubChStartAdr = 785;                  % DRS 4 News (DAB)
% SubChSize = 42;
% Audiokbps = 56;
% Protection = 3;
% UEP = true;

% -----------------------------------------------------------------------------------------
% Variablen und Felder Vorbereiten
% -----------------------------------------------------------------------------------------

lan = 0;                                                        % LAN brauchen

SymbolAnz = 76;                                                 % Anzahl Symbole in einem DAB Frame
Mode = 1;                                                       % Mode 1
N = 2^11;                                                       % Tu (Standard EN300401 Seite 145, durch Mode gegeben)
DurSymbol = 2552;                                               % Ts (Standard EN300401 Seite 145, durch Mode gegeben)
CarrierAnz = 1536;                                              % Anzahl Carrier (Standard EN300401 Seite 145, durch Mode gegeben)
Offset = 100;                                                   % FFT-Bereich in mitte des OFDM Symbols schieben (siehe Guard Time)
FreqIntTabSize = 2048;                                          % Grösse der Frequenz Interleaving Tabelle (Standard EN300401 Seite 145, durch Mode gegeben)

if UEP == true                                                  % Errorprotection von DAB anwenden
    [L1Range, L2Range, L3Range, L4Range, PI1, PI2, PI3, PI4, Padding] = UEPTab (Audiokbps, Protection);
    
else                                                            % Errorprotection von DAB+ anwenden
    [Audiokbps,PI1,PI2,L1Range,L2Range] = EEPTab (Protection,SubChSize);
end

DataLastRound = zeros(16,4*SubChSize*64);                       % Speicher für Time Interleaving
[InterleavingTab] = FreqInterleavingTab(FreqIntTabSize);        % Frequenzinterleaving Tabelle vorbereiten
DispSequenz = EnergyDispGen(100000);                            % Energy Dispersion Sequenz vorbereiten
DataEneChain = zeros(1,5*384*8);                                % Kette für Datenstrom aus der Energy Dispersion vorbereiten
DabFrameCount = 0;                                              % Framezähle am Ausgang der Energy Dispersion
SuperFrameSync = false;                                         % Synchronisation der Audio Super Frame überwachen
AllAudio = [];                                                  % Variable für Audiofile vorbereiten
ReadFile = fopen ('../Aufzeichnungen/Record1.dat', 'rb');                         % Quelldatenfile definieren
ReadSize = 150000;                                              % Anzahl Samples aus Quelldatenfile pro durchlauf lesen
fs_file = 2e6;                                                  % Samplingrate im Quellfile
fs = 2.048e6;                                                   % Samplingrate des Algorithmuses
trellis = poly2trellis(7,[133 171 145 133]);                    % Generatorpolynom für Trellis
fid = fopen('audio.mp2', 'w');                                  % Audiofile öffnen
OldData = [];                                                   % Noch nicht verarbeite Daten aus dem Datenstrom
au_start = 0;                                                   % Startposition der synchronen AccessUnit
num_aus = 0;                                                    % Anzahl Audiopackete in einem Superframe
read = true;                                                    % true = Noch weitere Daten im Quellfile vorhanden
FrameNr = 0;                                                    % Anzahl verarbeitete DAB Frames

% -----------------------------------------------------------------------------------------
% Netzwerk Socket öffnen und auf Verbindung warten
% -----------------------------------------------------------------------------------------

if lan == 1
    sSocket = ServerSocket(9999);                       % Audiodaten auf Port 9999 bereitstellen
    socket = sSocket.accept();
    out = socket.getOutputStream();
end

tic;

while read == true
    % -----------------------------------------------------------------------------------------
    % Stück des aufgezeichneten Files laden
    % -----------------------------------------------------------------------------------------
    try
        [NewData] = ComplexDataLoad(ReadFile,ReadSize,fs_file,fs);          % Komplexe Daten
    catch
        read = false;                                                       % Es konnte nicht mehr genügend Daten aus dem File gelesen werden
        break;
    end
    
    % -----------------------------------------------------------------------------------------
    % Framestart detektieren
    % -----------------------------------------------------------------------------------------
    
    [Signal OldData] = DetFrameStartStream2([OldData; NewData],Offset);     % Neue Daten an noch nicht gebrauchte Daten anhängen

    if ~isempty(Signal)                                                     % Signalverarbeitung wenn ein Framestart und genügend Daten detektiert wurden
        
        FrameNr = FrameNr +1;
        
        % -----------------------------------------------------------------------------------------
        % FFT des neusten Symbols
        % -----------------------------------------------------------------------------------------

        fft_Frame = SymbolFFTStream(Signal,SymbolAnz,CarrierAnz,DurSymbol,N);

        % -----------------------------------------------------------------------------------------
        % Frequency interleaving
        % -----------------------------------------------------------------------------------------

        [DeintFFTFrame] = FreqDeInterleaving(InterleavingTab,fft_Frame,FreqIntTabSize);


        % -----------------------------------------------------------------------------------------
        % Symbol demapper
        % -----------------------------------------------------------------------------------------

        Data = zeros(1,72*1536*2);                      % 73 - 1 = 72 Symbole im MSC (da differentiell)

        for f=1:SymbolAnz-1-3
            Data(1+(f-1)*CarrierAnz*2:(f)*CarrierAnz*2) = [real(DeintFFTFrame(f,:)) imag(DeintFFTFrame(f,:))];
        end

        % -----------------------------------------------------------------------------------------
        % Aus den 72 MSC Symbole, die 4 Convolutional codewords bilden
        % -----------------------------------------------------------------------------------------

        MSC = zeros(4,55296);

        for r=0:3
            MSC(r+1,:) = Data(r*55296+1:(r+1)*55296);
        end

        % -----------------------------------------------------------------------------------------
        % Sub-Channel herauslesen
        % -----------------------------------------------------------------------------------------

        SubChData(1:4,:) = MSC(:,64*SubChStartAdr+1:64*(SubChStartAdr+SubChSize));                 % Daten eines SubChannels (Vermerk: Matlab indexierung +1)


        % -----------------------------------------------------------------------------------------
        % Unterscheidung DAB oder DAB+
        % -----------------------------------------------------------------------------------------
        if UEP == true                                                                     % DAB

            % -----------------------------------------------------------------------------------------
            % Time interleaving
            % -----------------------------------------------------------------------------------------

            [TiIntSubChData, DataLastRound] = TimeInterleavingStream(SubChData,SubChSize,DataLastRound);

            % -----------------------------------------------------------------------------------------
            % (De)puncturing
            % -----------------------------------------------------------------------------------------

            DataDep = [depuncturing(TiIntSubChData(:,1:L1Range),PI1)...
                       depuncturing(TiIntSubChData(:,L1Range+1:L2Range),PI2)...
                       depuncturing(TiIntSubChData(:,L2Range+1:L3Range),PI3)...
                       depuncturing(TiIntSubChData(:,L3Range+1:L4Range),PI4)...
                       depuncturing(TiIntSubChData(:,L4Range+1:L4Range+12),8)];               % Tail

            % -----------------------------------------------------------------------------------------
            % Viterbi Decoder
            % -----------------------------------------------------------------------------------------

            DataVit = zeros(length(DataDep(:,1)),length(DataDep(1,:))/4+1);                   % Audio-Bitvektor + Tail (6) + Matlab Viterbi (1)

            for f=1:length(DataDep(:,1))

                DataVit(f,:) = vitdec([DataDep(f,:) 0 0 0 0],trellis,1,'cont','unquant');

            end

            DataVit = DataVit(:,2:end-6);      % Tail wegnehmen

            % -----------------------------------------------------------------------------------------
            % Energy dispersal
            % -----------------------------------------------------------------------------------------

            DataEne = zeros(size(DataVit));
            for m=1:length(DataEne(:,1))
                DataEne(m,:) = xor(DataVit(m,:),DispSequenz(1:length(DataEne(1,:))));       % XOR Verknüpfung mit generierter Sequenz
            end

            % -----------------------------------------------------------------------------------------
            % Audiodaten bilden
            % -----------------------------------------------------------------------------------------

            Audio=(reshape(DataEne',8,[])'*[128 64 32 16 8 4 2 1]')';                       % Bitdaten zu Bytedaten umwandeln

            % -----------------------------------------------------------------------------------------
            % TCP
            % -----------------------------------------------------------------------------------------

            if FrameNr >= 6
                fwrite(fid,Audio, 'uint8');                                                 % Bytedaten in File speichern
                if lan == 1
                    out.write(Audio,0,length(Audio));
                    out.flush();
                end
            end


        else                                                                               % DAB+

            % -----------------------------------------------------------------------------------------
            % Time interleaving
            % -----------------------------------------------------------------------------------------

            [TiIntSubChData, DataLastRound] = TimeInterleavingStream(SubChData,SubChSize,DataLastRound);

            % -----------------------------------------------------------------------------------------
            % (De)puncturing
            % -----------------------------------------------------------------------------------------

            DataDep = [depuncturing(TiIntSubChData(:,1:L1Range),PI1)...
                       depuncturing(TiIntSubChData(:,L1Range+1:L2Range),PI2)...
                       depuncturing(TiIntSubChData(:,L2Range+1:L2Range+12),8)];             % Tail

            % -----------------------------------------------------------------------------------------
            % Viterbi Decoder
            % -----------------------------------------------------------------------------------------

            DataVit = zeros(length(DataDep(:,1)),length(DataDep(1,:))/4+1);                   % Audio-Bitvektor + Tail (6) + Matlab Viterbi (1)

            trellis = poly2trellis(7,[133 171 145 133]);

            for f=1:length(DataDep(:,1))

                DataVit(f,:) = vitdec([DataDep(f,:) 0 0 0 0],trellis,1,'cont','unquant');

            end

            DataVit = DataVit(:,2:end-6);      % Tail wegnehmen

            % -----------------------------------------------------------------------------------------
            % Energy dispersal
            % -----------------------------------------------------------------------------------------

            DataEne = zeros(size(DataVit));
            for m=1:length(DataEne(:,1))
                DataEne(m,:) = xor(DataVit(m,:),DispSequenz(1:length(DataEne(1,:))));
            end

            % -----------------------------------------------------------------------------------------
            % Super Frame Handling
            % ----------------------------------------------------------------------------------------- 

            DataEneChain(96*8*DabFrameCount+1:96*8*(DabFrameCount+4)) = reshape(DataEne',1,[]);         % Wörter Chain

            if FrameNr >= 6
                [DabFrameCount,SuperFrameSync,DataEneChain,au_start,num_aus] = SuperFrameHandling(DabFrameCount,SuperFrameSync,DataEneChain,au_start,Audiokbps,lan,num_aus);
            end
        end
    end
end

fclose (ReadFile);
fclose(fid);

if lan == 1
socket.close();
sSocket.close();
end

fprintf('alles berechnen %3i Sek \n',round(toc));