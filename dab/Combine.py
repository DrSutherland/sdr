#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Thu May 19 13:22:16 2011
##################################################

from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import trellis
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import wx
import howto
import time
import sys

class top_block(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		
		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 2000000
		fftsize = 2048

		##################################################
		# Blocks
		##################################################
		
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="addr=192.168.10.2",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		# Quelle
		
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(227360000, 0) # 194064000,227360000
		self.uhd_usrp_source_0.set_gain(31.5, 0)
		
		self.throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate*1)
		
		# Resampler fuer 2.000 MS/s -> 2.048 MS/s
		self.blks2_rational_resampler_xxx_0 = blks2.rational_resampler_ccc(
			interpolation=128,
			decimation=125,
			taps=None,
			fractional_bw=None,
		)
		
		# Framestarts detektieren
		self.framestart_detecter_cc = howto.framestart_detecter_cc(fftsize,504,76)
		
		# OFDM Symbole herausarbeiten
		self.ofdm_symbole = howto.ofdm_symbol_cutter_cc(196608,fftsize,504,76,150)
		
		# FFT des Symbols bilden
		self.s2v = gr.stream_to_vector(gr.sizeof_gr_complex, 2048)
		
		# FFT eines Symbols
		self.fft_vcc = gr.fft_vcc(fftsize, 		# FFT groesse
			True, 								# forward FFT
			[], 								# Window
			True)								# Shift
		
		# Symbol-Differenz bilden
		self.diff = howto.de_diff_mod_vcc(fftsize,256)
		
		# Anzeige der Modulation
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=791,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=True,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		
		
		
		self.freq_interl = howto.de_freq_interleaver_vcf(2048,1536)			# FFT Size = 2048, Subcarrier = 1536
		
		self.null_symbol_resample = howto.null_symbol_resample_bb(2048)		# Anpassung fuer Mode 1 erzeugen
		
		self.subCha = howto.sub_channel_vff(1536,188,84)					# Subcarrier = 1536
		
		self.v2s_msc = gr.vector_to_stream(gr.sizeof_float, 84*64/8)		# Abfluss fuer MSC
		self.vector_sink_msc = gr.null_sink(gr.sizeof_float*1)
		
		self.bonder = howto.bonder_vff(2304/8,2304)
		self.depunct_fic = howto.depuncturing_vff(36,16,21,15,3,1,0,1,0)	# Depuncturing
		
		self.viterbi = howto.viterbi_vfb(3096)								# Viterbi
		
		self.energy_disp_fic = howto.energy_disp_vbb(774)					# Energy dispersal anwenden
		
		self.fib_cutter = howto.cutter_vbb(768,256)							# FIBs bilden
		
		fib_crc16 = howto.fib_crc16_vbb(256)								# CRC Check
		
		self.fib_sink = howto.fib_sink3_vbf()								# FIC Informationen auslesen
		
		self.dst_0 = gr.vector_sink_f()										# Datenbank
		
		##################################################
		# Connections
		##################################################
		
		self.connect((self.uhd_usrp_source_0, 0), self.blks2_rational_resampler_xxx_0)
		
		self.connect(self.blks2_rational_resampler_xxx_0, self.framestart_detecter_cc, (self.ofdm_symbole,1))	# Framestart detektion
		self.connect(self.blks2_rational_resampler_xxx_0, (self.ofdm_symbole,0))								# Symbole herausarbeiten
		self.connect((self.ofdm_symbole,0), self.s2v, self.fft_vcc, self.diff)									# FFT und Div Demod
		self.connect((self.diff, 1), (self.wxgui_scopesink2_0, 0))												# Modulationsgrafik
		
		
		self.connect((self.ofdm_symbole,1), self.null_symbol_resample, (self.subCha,1))	# Framestart-Signalisierung
		self.connect((self.diff, 0), self.freq_interl)								# Frequenz interleaving
		self.connect(self.freq_interl, (self.subCha,0))								# MSC und FIC bilden'''
		
		self.connect((self.subCha,0), self.v2s_msc, self.vector_sink_msc)			# MSC
		
		self.connect((self.subCha,1), self.bonder)									# FIC zusammensetzen
		self.connect(self.bonder, self.depunct_fic)
		self.connect(self.depunct_fic, self.viterbi)								# Depuncturing
		self.connect(self.viterbi, self.energy_disp_fic)							# Viterbi
		self.connect(self.energy_disp_fic, self.fib_cutter)							# Energy Dispersal
		self.connect(self.fib_cutter, fib_crc16)									# FIBs bilden
		self.connect(fib_crc16, self.fib_sink)										# FIB Sink
		self.connect(self.fib_sink, self.dst_0)											# Datenbank fuellen
		
	def dataout(self):
		
		result_data0 = self.dst_0.data ()
		return result_data0

class music(grc_wxgui.top_block_gui):
	def __init__(self,StartAdr,SizeCU,Level,kbps):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		
		TabPunct = [[ 32, 5,  3,  4,  17, 0,  5,  3,  2,  1, 0],				# Tabelle fuer Depuncturing ETSI EN 300 401 Seite 134
		            [ 32, 4,  3,  3,  18, 0, 11,  6,  5,  1, 0],
		            [ 32, 3,  3,  4,  14, 3, 15,  9,  6,  8, 0],
		            [ 32, 2,  3,  4,  14, 3, 22, 13,  8, 13, 0],
		            [ 32, 1,  3,  5,  13, 3, 24, 17, 12, 17, 4],
		            [ 48, 5,  4,  3,  26, 3,  5,  4,  2,  3, 0],
		            [ 48, 4,  3,  4,  26, 3,  9,  6,  4,  6, 0],
		            [ 48, 3,  3,  4,  26, 3, 15, 10,  6,  9, 4],
		            [ 48, 2,  3,  4,  26, 3, 24, 14,  8, 15, 0],
		            [ 48, 1,  3,  5,  25, 3, 24, 18, 13, 18, 0],
		            [ 56, 5,  6, 10,  23, 3,  5,  4,  2,  3, 0],
		            [ 56, 4,  6, 10,  23, 3,  9,  6,  4,  5, 0],
		            [ 56, 3,  6, 12,  21, 3, 16,  7,  6,  9, 0],
		            [ 56, 2,  6, 10,  23, 3, 23, 13,  8, 13, 8],
		            [ 64, 5,  6,  9,  31, 2,  5,  3,  2,  3, 0],
		            [ 64, 4,  6,  9,  33, 0, 11,  6,  5,  1, 0],
		            [ 64, 3,  6, 12,  27, 3, 16,  8,  6,  9, 0],
		            [ 64, 2,  6, 10,  29, 3, 23, 13,  8, 13, 8],
		            [ 64, 1,  6, 11,  28, 3, 24, 18, 12, 18, 4],
		            [ 80, 5,  6, 10,  41, 3,  6,  3,  2,  3, 0],
		            [ 80, 4,  6, 10,  41, 3, 11,  6,  5,  6, 0],
		            [ 80, 3,  6, 11,  40, 3, 16,  8,  6,  7, 0],
		            [ 80, 2,  6, 10,  41, 3, 23, 13,  8, 13, 8],
		            [ 80, 1,  6, 10,  41, 3, 24, 17, 12, 18, 4],
		            [ 96, 5,  7,  9,  53, 3,  5,  4,  2,  4, 0],
		            [ 96, 4,  7, 10,  52, 3,  9,  6,  4,  6, 0],
		            [ 96, 3,  6, 12,  51, 3, 16,  9,  6, 10, 4],
		            [ 96, 2,  6, 10,  53, 3, 22, 12,  9, 12, 0],
		            [ 96, 1,  6, 13,  50, 3, 24, 18, 13, 19, 0],
		            [112, 5, 14, 17,  50, 3,  5,  4,  2,  5, 0],
		            [112, 4, 11, 21,  49, 3,  9,  6,  4,  8, 0],
		            [112, 3, 11, 23,  47, 3, 16,  8,  6,  9, 0],
		            [112, 2, 11, 21,  49, 3, 23, 12,  9, 14, 4],
		            [128, 5, 12, 19,  62, 3,  5,  3,  2,  4, 0],
		            [128, 4, 11, 21,  61, 3, 11,  6,  5,  7, 0],
		            [128, 3, 11, 22,  60, 3, 16,  9,  6, 10, 4],
		            [128, 2, 11, 21,  61, 3, 22, 12,  9, 14, 0],
		            [128, 1, 11, 20,  62, 3, 24, 17, 13, 19, 8],
		            [160, 5, 11, 19,  87, 3,  5,  4,  2,  4, 0],
		            [160, 4, 11, 23,  83, 3, 11,  6,  5,  9, 0],
		            [160, 3, 11, 24,  82, 3, 16,  8,  6, 11, 0],
		            [160, 2, 11, 21,  85, 3, 22, 11,  9, 13, 0],
		            [160, 1, 11, 22,  84, 3, 24, 18, 12, 19, 0],
		            [192, 5, 11, 20, 110, 3,  6,  4,  2,  5, 0],
		            [192, 4, 11, 22, 108, 3, 10,  6,  4,  9, 0],
		            [192, 3, 11, 24, 106, 3, 16, 10,  6, 11, 0],
		            [192, 2, 11, 20, 110, 3, 22, 13,  9, 13, 8],
		            [192, 1, 11, 21, 109, 3, 24, 20, 13, 24, 0],
		            [224, 5, 12, 22, 131, 3,  8,  6,  2,  6, 4],
		            [224, 4, 12, 26, 127, 3, 12,  8,  4, 11, 0],
		            [224, 3, 11, 20, 134, 3, 16, 10,  7,  9, 0],
		            [224, 2, 11, 22, 132, 3, 24, 16, 10, 15, 0],
		            [224, 1, 11, 24, 130, 3, 24, 20, 12, 20, 4],
		            [256, 5, 11, 24, 154, 3,  6,  5,  2,  5, 0],
		            [256, 4, 11, 24, 154, 3, 12,  9,  5, 10, 4],
		            [256, 3, 11, 27, 151, 3, 16, 10,  7, 10, 0],
		            [256, 2, 11, 22, 156, 3, 24, 14, 10, 13, 8],
		            [256, 1, 11, 26, 152, 3, 24, 19, 14, 18,4],
		            [320, 5, 11, 26, 200, 3,  8,  5,  2,  6,4],
		            [320, 4, 11, 25, 201, 3, 13,  9,  5, 10,8],
		            [320, 2, 11, 26, 200, 3, 24, 17,  9, 17,0],
		            [384, 5, 11, 27, 247, 3,  8,  6,  2,  7,0],
		            [384, 3, 11, 24, 250, 3, 16,  9,  7, 10,4],
		            [384, 1, 12, 28, 245, 3, 24, 20, 14, 23,8]]
		            
		for x in range(64): 											# Werte aus Tabelle herauslesen
			if (TabPunct[x][0]==kbps) and (TabPunct[x][1]==Level):
				L1 = TabPunct[x][2]
				L2 = TabPunct[x][3]
				L3 = TabPunct[x][4]
				L4 = TabPunct[x][5]
				PI1 = TabPunct[x][6]
				PI2 = TabPunct[x][7]
				PI3 = TabPunct[x][8]
				PI4 = TabPunct[x][9]
		
		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 2000000
		fftsize = 2048

		##################################################
		# Blocks
		##################################################
		
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="addr=192.168.10.2",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		# Quelle
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(227360000, 0) # 194064000,227360000
		self.uhd_usrp_source_0.set_gain(31.5, 0)
		
		self.throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate*1)
		
		# Resampler fuer 2.000 MS/s -> 2.048 MS/s
		self.blks2_rational_resampler_xxx_0 = blks2.rational_resampler_ccc(
			interpolation=128,
			decimation=125,
			taps=None,
			fractional_bw=None,
		)
		
		# Framestarts detektieren
		self.framestart_detecter_cc = howto.framestart_detecter_cc(fftsize,504,76)
		
		# OFDM Symbole herausarbeiten
		self.ofdm_symbole = howto.ofdm_symbol_cutter_cc(196608,fftsize,504,76,150)
		
		# FFT des Symbols bilden
		self.s2v = gr.stream_to_vector(gr.sizeof_gr_complex, 2048)
		
		# FFT eines Symbols
		self.fft_vcc = gr.fft_vcc(fftsize, 		# FFT groesse
			True, 								# forward FFT
			[], 								# Window
			True)								# Shift
		
		# Symbol-Differenz bilden
		self.diff = howto.de_diff_mod_vcc(fftsize,256)
		
		# Anzeige der Modulation
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=791,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=True,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		
		
		
		self.freq_interl = howto.de_freq_interleaver_vcf(2048,1536)			# FFT Size = 2048, Subcarrier = 1536
		
		self.null_symbol_resample = howto.null_symbol_resample_bb(2048)		# Anpassung fuer Mode 1 erzeugen
		
		self.subCha = howto.sub_channel_vff(1536,StartAdr,SizeCU)			# Subcarrier = 1536
		
		self.timeInt = howto.time_interleaving_vff(SizeCU)					# Time Interleaving
		
		self.depunct_fic = howto.depuncturing_vff(SizeCU,PI1,L1,PI2,L2,PI3,L3,PI4,L4)	# Depuncturing
		
		self.viterbi = howto.viterbi_vfb((L1+L2+L3+L4)*32*4+4*6)						# Viterbi + Tail
		
		self.energy_disp = howto.energy_disp_vbb((L1+L2+L3+L4)*32+6)					# Energy dispersal anwenden
		
		self.prearrangement = howto.prearrangement_vbb((L1+L2+L3+L4)*32)				# Bitwert zu Bytewert umwandeln
		
		self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(										# TCP Abfluss
			itemsize=gr.sizeof_char*1,
			addr="127.0.0.1",
			port=9999,
			server=True,
		)
		
		##################################################
		# Connections
		##################################################
		
		self.connect((self.uhd_usrp_source_0, 0), self.blks2_rational_resampler_xxx_0)
		
		self.connect(self.blks2_rational_resampler_xxx_0, self.framestart_detecter_cc, (self.ofdm_symbole,1))	# Framestart detektion
		self.connect(self.blks2_rational_resampler_xxx_0, (self.ofdm_symbole,0))								# Symbole herausarbeiten
		self.connect((self.ofdm_symbole,0), self.s2v, self.fft_vcc, self.diff)									# FFT und Div Demod
		self.connect((self.diff, 1), (self.wxgui_scopesink2_0, 0))												# Modulationsgrafik
		
		
		self.connect((self.ofdm_symbole,1), self.null_symbol_resample, (self.subCha,1))	# Framestart-Signalisierung
		self.connect((self.diff, 0), self.freq_interl)									# Frequenz interleaving
		self.connect(self.freq_interl, (self.subCha,0))									# MSC und FIC bilden'''
		
		self.connect((self.subCha,0), self.timeInt)										# MSC
		self.connect(self.timeInt, self.depunct_fic)									# Time interleaving
		self.connect(self.depunct_fic, self.viterbi)									# Depuncturing
		self.connect(self.viterbi,self.energy_disp)										# Viterbi
		self.connect(self.energy_disp,self.prearrangement)								# Energy dispersal
		self.connect(self.prearrangement,self.blks2_tcp_sink_0)							# Prearrangement fuer TCP
		
		self.v2s = gr.vector_to_stream(gr.sizeof_float, 2304/8)
		self.vector_sink_f = gr.vector_sink_f(1)		#test
		self.connect((self.subCha,1), self.v2s, self.vector_sink_f)					# Test


if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.start()								# FIC Datenbank erstellen
	time.sleep(3)
	tb.stop()								# FIC Datenbankerstellung beenden
	
	# Daten des gewuenschten Senders aus Datenbank herauslesen
	SenderDatenbank = tb.dataout()
	Startindex = len(SenderDatenbank) - len(SenderDatenbank)%6
	kbps=0
	print "\n\n\n\n\n                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	while (kbps==0):
		Sender = input("                          Choose a DAB subchannel (DAB+ not allowed): ")
		print "                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		for x in range(Startindex):
			if (x%6 == 0) and (SenderDatenbank[x] == Sender):
				StartAdr = int(round(SenderDatenbank[x+2]))
				SizeCU = int(round(SenderDatenbank[x+3]))
				Level = int(round(SenderDatenbank[x+4]))
				kbps = int(round(SenderDatenbank[x+5]))
	print "                         ! Connect Musikplayer to TCP 127.0.0.1:9999 !"
	print "                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	ta = music(StartAdr,SizeCU,Level,kbps)
	ta.Run(True)			# Musiksender Abspielen
	sys.exit(0)
