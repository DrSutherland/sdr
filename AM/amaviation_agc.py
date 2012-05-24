#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Amaviation Agc
# Generated: Tue May 22 20:49:45 2012
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import baz
import wx

class amaviation_agc(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Amaviation Agc")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.sql_threshold = sql_threshold = -30
		self.samp_rate = samp_rate = 1000000
		self.frq_offset = frq_offset = 0
		self.base_frq = base_frq = 131725000

		##################################################
		# Blocks
		##################################################
		_sql_threshold_sizer = wx.BoxSizer(wx.VERTICAL)
		self._sql_threshold_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_sql_threshold_sizer,
			value=self.sql_threshold,
			callback=self.set_sql_threshold,
			label="Squelch Threshold",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._sql_threshold_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_sql_threshold_sizer,
			value=self.sql_threshold,
			callback=self.set_sql_threshold,
			minimum=-100,
			maximum=0,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_sql_threshold_sizer)
		_frq_offset_sizer = wx.BoxSizer(wx.VERTICAL)
		self._frq_offset_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_frq_offset_sizer,
			value=self.frq_offset,
			callback=self.set_frq_offset,
			label="Frequency Offset",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._frq_offset_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_frq_offset_sizer,
			value=self.frq_offset,
			callback=self.set_frq_offset,
			minimum=-100000,
			maximum=100000,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_frq_offset_sizer)
		self._base_frq_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.base_frq,
			callback=self.set_base_frq,
			label="Base frequency",
			converter=forms.float_converter(),
		)
		self.Add(self._base_frq_text_box)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.Add(self.wxgui_fftsink2_0.win)
		self.rtl2832_source_0 = baz.rtl_source_c(defer_creation=True)
		self.rtl2832_source_0.set_verbose(True)
		self.rtl2832_source_0.set_vid(0x0)
		self.rtl2832_source_0.set_pid(0x0)
		self.rtl2832_source_0.set_tuner_name("")
		self.rtl2832_source_0.set_default_timeout(0)
		self.rtl2832_source_0.set_use_buffer(True)
		self.rtl2832_source_0.set_fir_coefficients(([]))
		
		
		
		
		
		if self.rtl2832_source_0.create() == False: raise Exception("Failed to create RTL2832 Source: rtl2832_source_0")
		
		self.rtl2832_source_0.set_bandwidth(300000)
		
		self.rtl2832_source_0.set_sample_rate(samp_rate)
		
		self.rtl2832_source_0.set_frequency(base_frq+frq_offset)
		
		self.rtl2832_source_0.set_gain_mode("sensitive")
		
		self.rtl2832_source_0.set_auto_gain_mode(False)
		self.rtl2832_source_0.set_relative_gain(True)
		self.rtl2832_source_0.set_gain(30)
		  
		self.gr_simple_squelch_cc_0 = gr.simple_squelch_cc(sql_threshold, 0.0001)
		self.gr_agc2_xx_0 = gr.agc2_cc(100e-3, 200e-3, 1.0, 1.0, 2.0)
		self.blks2_rational_resampler_xxx_0 = blks2.rational_resampler_ccc(
			interpolation=48,
			decimation=1000,
			taps=None,
			fractional_bw=None,
		)
		self.blks2_am_demod_cf_0 = blks2.am_demod_cf(
			channel_rate=48000,
			audio_decim=1,
			audio_pass=5000,
			audio_stop=5500,
		)
		self.audio_sink_0 = audio.sink(48000, "hw:1,0", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.rtl2832_source_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.blks2_am_demod_cf_0, 0), (self.audio_sink_0, 0))
		self.connect((self.blks2_rational_resampler_xxx_0, 0), (self.gr_simple_squelch_cc_0, 0))
		self.connect((self.gr_simple_squelch_cc_0, 0), (self.gr_agc2_xx_0, 0))
		self.connect((self.gr_agc2_xx_0, 0), (self.blks2_am_demod_cf_0, 0))
		self.connect((self.rtl2832_source_0, 0), (self.blks2_rational_resampler_xxx_0, 0))

	def get_sql_threshold(self):
		return self.sql_threshold

	def set_sql_threshold(self, sql_threshold):
		self.sql_threshold = sql_threshold
		self._sql_threshold_slider.set_value(self.sql_threshold)
		self._sql_threshold_text_box.set_value(self.sql_threshold)
		self.gr_simple_squelch_cc_0.set_threshold(self.sql_threshold)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.rtl2832_source_0.set_sample_rate(self.samp_rate)

	def get_frq_offset(self):
		return self.frq_offset

	def set_frq_offset(self, frq_offset):
		self.frq_offset = frq_offset
		self._frq_offset_slider.set_value(self.frq_offset)
		self._frq_offset_text_box.set_value(self.frq_offset)
		self.rtl2832_source_0.set_frequency(self.base_frq+self.frq_offset)

	def get_base_frq(self):
		return self.base_frq

	def set_base_frq(self, base_frq):
		self.base_frq = base_frq
		self._base_frq_text_box.set_value(self.base_frq)
		self.rtl2832_source_0.set_frequency(self.base_frq+self.frq_offset)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = amaviation_agc()
	tb.Run(True)

