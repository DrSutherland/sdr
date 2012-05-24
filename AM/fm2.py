#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Fm2
# Generated: Fri May 18 17:12:31 2012
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import baz
import wx

class fm2(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Fm2")
		_icon_path = "/usr/local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 1000000
		self.frq_offset = frq_offset = 0
		self.base_freq_slider = base_freq_slider = 88.5e6

		##################################################
		# Blocks
		##################################################
		_frq_offset_sizer = wx.BoxSizer(wx.VERTICAL)
		self._frq_offset_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_frq_offset_sizer,
			value=self.frq_offset,
			callback=self.set_frq_offset,
			label='frq_offset',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._frq_offset_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_frq_offset_sizer,
			value=self.frq_offset,
			callback=self.set_frq_offset,
			minimum=-200000,
			maximum=200000,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_frq_offset_sizer)
		_base_freq_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._base_freq_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_base_freq_slider_sizer,
			value=self.base_freq_slider,
			callback=self.set_base_freq_slider,
			label='base_freq_slider',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._base_freq_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_base_freq_slider_sizer,
			value=self.base_freq_slider,
			callback=self.set_base_freq_slider,
			minimum=88e6,
			maximum=108e6,
			num_steps=400,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_base_freq_slider_sizer)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.GetWin(),
			baseband_freq=0,
			dynamic_range=100,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=2,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
		)
		self.Add(self.wxgui_waterfallsink2_0.win)
		self.rtl2832_source_0 = baz.rtl_source_c(defer_creation=True)
		self.rtl2832_source_0.set_verbose(True)
		self.rtl2832_source_0.set_vid(0x0)
		self.rtl2832_source_0.set_pid(0x0)
		self.rtl2832_source_0.set_tuner_name("")
		self.rtl2832_source_0.set_default_timeout(0)
		self.rtl2832_source_0.set_use_buffer(True)
		self.rtl2832_source_0.set_fir_coefficients(([]))
		
		
		
		
		
		if self.rtl2832_source_0.create() == False: raise Exception("Failed to create RTL2832 Source: rtl2832_source_0")
		
		self.rtl2832_source_0.set_bandwidth(200000)
		
		self.rtl2832_source_0.set_sample_rate(samp_rate)
		
		self.rtl2832_source_0.set_frequency(base_freq_slider)
		
		
		self.rtl2832_source_0.set_auto_gain_mode(False)
		self.rtl2832_source_0.set_relative_gain(True)
		self.rtl2832_source_0.set_gain(1)
		  
		self.gr_freq_xlating_fir_filter_xxx_0 = gr.freq_xlating_fir_filter_ccc(1, (10, ), frq_offset, samp_rate)
		self.blks2_wfm_rcv_0 = blks2.wfm_rcv(
			quad_rate=48000,
			audio_decimation=1,
		)
		self.blks2_rational_resampler_xxx_0 = blks2.rational_resampler_ccc(
			interpolation=48000,
			decimation=1000000,
			taps=None,
			fractional_bw=None,
		)
		self.audio_sink_0 = audio.sink(48000, "pulse", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.blks2_rational_resampler_xxx_0, 0), (self.blks2_wfm_rcv_0, 0))
		self.connect((self.blks2_wfm_rcv_0, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.blks2_rational_resampler_xxx_0, 0))
		self.connect((self.rtl2832_source_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.rtl2832_source_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

	def get_frq_offset(self):
		return self.frq_offset

	def set_frq_offset(self, frq_offset):
		self.frq_offset = frq_offset
		self._frq_offset_slider.set_value(self.frq_offset)
		self._frq_offset_text_box.set_value(self.frq_offset)
		self.gr_freq_xlating_fir_filter_xxx_0.set_center_freq(self.frq_offset)

	def get_base_freq_slider(self):
		return self.base_freq_slider

	def set_base_freq_slider(self, base_freq_slider):
		self.base_freq_slider = base_freq_slider
		self.rtl2832_source_0.set_frequency(self.base_freq_slider)
		self._base_freq_slider_slider.set_value(self.base_freq_slider)
		self._base_freq_slider_text_box.set_value(self.base_freq_slider)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = fm2()
	tb.Run(True)

