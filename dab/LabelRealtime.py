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
from optparse import OptionParser
import wx
import howto
import time
import baz

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
		self.rtl2832_source_0 = baz.rtl_source_c(defer_creation=True)
		self.rtl2832_source_0.set_verbose(True)
		self.rtl2832_source_0.set_vid(0x0)
		self.rtl2832_source_0.set_pid(0x0)
		self.rtl2832_source_0.set_tuner_name("")
		self.rtl2832_source_0.set_default_timeout(0)
		self.rtl2832_source_0.set_use_buffer(True)
		self.rtl2832_source_0.set_fir_coefficients(([]))
		
		if self.rtl2832_source_0.create() == False: raise Exception("Failed to create RTL2832 Source: rtl2832_source_0")
		
		
		self.rtl2832_source_0.set_sample_rate(samp_rate)
		
		self.rtl2832_source_0.set_frequency(225648000)
		
		self.rtl2832_source_0.set_auto_gain_mode(False)
		self.rtl2832_source_0.set_relative_gain(True)
		self.rtl2832_source_0.set_gain(3)
				
		#self.rtl2832_source_0 = uhd.usrp_source(
		#	device_addr="addr=192.168.10.2",
		#	io_type=uhd.io_type.COMPLEX_FLOAT32,
		#	num_channels=1,
		#)

		
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
		
		fib_crc16 = howto.fib_crc16_vbb(256)								# CRC Check erzeugen
		
		self.fib_sink = howto.fib_sink_vb()									# Serviceanzeige auf Konsole initialisieren
		
		##################################################
		# Connections
		##################################################
		
		self.connect((self.rtl2832_source_0, 0), self.blks2_rational_resampler_xxx_0)
		
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
		

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.Run(True)
