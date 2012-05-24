#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: rtl-sdr
# Author: louis
# Description: http://sdr.osmocom.org/trac/wiki/rtl-sdr
# Generated: Fri May 18 12:18:17 2012
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

class rtlsdr_direct(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="rtl-sdr")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.xlate_tune = xlate_tune = 0
		self.samp_rate = samp_rate = 1024000
		self.noxon_central_freq = noxon_central_freq = 103e6
		self.rx_freq = rx_freq = noxon_central_freq+xlate_tune
		self.filter_taps = filter_taps = firdes.low_pass(1,samp_rate,100e3,1e3)
		self.af_gain = af_gain = 3

		##################################################
		# Blocks
		##################################################
		_xlate_tune_sizer = wx.BoxSizer(wx.VERTICAL)
		self._xlate_tune_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_xlate_tune_sizer,
			value=self.xlate_tune,
			callback=self.set_xlate_tune,
			label="xlate tune",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._xlate_tune_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_xlate_tune_sizer,
			value=self.xlate_tune,
			callback=self.set_xlate_tune,
			minimum=-500e3,
			maximum=+500e3,
			num_steps=500,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_xlate_tune_sizer, 0, 0, 1, 1)
		self._noxon_central_freq_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.noxon_central_freq,
			callback=self.set_noxon_central_freq,
			label="Noxon central frequency ",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._noxon_central_freq_static_text, 1, 0, 1, 1)
		_af_gain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._af_gain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_af_gain_sizer,
			value=self.af_gain,
			callback=self.set_af_gain,
			label="AF gain",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._af_gain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_af_gain_sizer,
			value=self.af_gain,
			callback=self.set_af_gain,
			minimum=0,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_af_gain_sizer, 0, 2, 1, 1)
		self.xlating_fir_filter = gr.freq_xlating_fir_filter_ccc(4, (filter_taps), -xlate_tune, samp_rate)
		self.wfm_rcv = blks2.wfm_rcv(
			quad_rate=samp_rate/4,
			audio_decimation=5,
		)
		self._rx_freq_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.rx_freq,
			callback=self.set_rx_freq,
			label="rx frequency ",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._rx_freq_static_text, 1, 3, 1, 1)
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
		
		self.rtl2832_source_0.set_frequency(102722000)
		
		
		self.rtl2832_source_0.set_auto_gain_mode(False)
		self.rtl2832_source_0.set_relative_gain(True)
		self.rtl2832_source_0.set_gain(3)
		  
		self.rr_stereo_right = blks2.rational_resampler_fff(
			interpolation=48,
			decimation=50,
			taps=None,
			fractional_bw=None,
		)
		self.fftsink_rf_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=noxon_central_freq,
			y_per_div=5,
			y_divs=10,
			ref_level=0,
			ref_scale=.5,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=10,
			average=True,
			avg_alpha=0.25,
			title="Total bandwidth",
			peak_hold=False,
			win=window.blackmanharris,
			size=(800,200),
		)
		self.Add(self.fftsink_rf_0.win)
		self.fftsink_rf = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=5,
			y_divs=10,
			ref_level=0,
			ref_scale=.5,
			sample_rate=samp_rate/4,
			fft_size=1024,
			fft_rate=10,
			average=True,
			avg_alpha=0.25,
			title="Baseband",
			peak_hold=False,
			size=(800,200),
		)
		self.Add(self.fftsink_rf.win)
		self.audio_sink = audio.sink(48000, "pulse", True)
		self.af_gain_stereo_left = gr.multiply_const_vff((af_gain, ))

		##################################################
		# Connections
		##################################################
		self.connect((self.xlating_fir_filter, 0), (self.fftsink_rf, 0))
		self.connect((self.af_gain_stereo_left, 0), (self.audio_sink, 0))
		self.connect((self.wfm_rcv, 0), (self.rr_stereo_right, 0))
		self.connect((self.xlating_fir_filter, 0), (self.wfm_rcv, 0))
		self.connect((self.rr_stereo_right, 0), (self.af_gain_stereo_left, 0))
		self.connect((self.af_gain_stereo_left, 0), (self.audio_sink, 1))
		self.connect((self.xlating_fir_filter, 0), (self.fftsink_rf_0, 0))
		self.connect((self.rtl2832_source_0, 0), (self.xlating_fir_filter, 0))

	def get_xlate_tune(self):
		return self.xlate_tune

	def set_xlate_tune(self, xlate_tune):
		self.xlate_tune = xlate_tune
		self.set_rx_freq(self.noxon_central_freq+self.xlate_tune)
		self._xlate_tune_slider.set_value(self.xlate_tune)
		self._xlate_tune_text_box.set_value(self.xlate_tune)
		self.xlating_fir_filter.set_center_freq(-self.xlate_tune)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_filter_taps(firdes.low_pass(1,self.samp_rate,100e3,1e3))
		self.fftsink_rf.set_sample_rate(self.samp_rate/4)
		self.fftsink_rf_0.set_sample_rate(self.samp_rate)
		self.rtl2832_source_0.set_sample_rate(self.samp_rate)

	def get_noxon_central_freq(self):
		return self.noxon_central_freq

	def set_noxon_central_freq(self, noxon_central_freq):
		self.noxon_central_freq = noxon_central_freq
		self._noxon_central_freq_static_text.set_value(self.noxon_central_freq)
		self.set_rx_freq(self.noxon_central_freq+self.xlate_tune)
		self.fftsink_rf_0.set_baseband_freq(self.noxon_central_freq)

	def get_rx_freq(self):
		return self.rx_freq

	def set_rx_freq(self, rx_freq):
		self.rx_freq = rx_freq
		self._rx_freq_static_text.set_value(self.rx_freq)

	def get_filter_taps(self):
		return self.filter_taps

	def set_filter_taps(self, filter_taps):
		self.filter_taps = filter_taps
		self.xlating_fir_filter.set_taps((self.filter_taps))

	def get_af_gain(self):
		return self.af_gain

	def set_af_gain(self, af_gain):
		self.af_gain = af_gain
		self._af_gain_slider.set_value(self.af_gain)
		self._af_gain_text_box.set_value(self.af_gain)
		self.af_gain_stereo_left.set_k((self.af_gain, ))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = rtlsdr_direct()
	tb.Run(True)

