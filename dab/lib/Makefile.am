#
# Copyright 2004,2005,2006,2008,2009,2010 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

include $(top_srcdir)/Makefile.common

# list of programs run by "make check" and "make distcheck"
TESTS = test_all

# ----------------------------------------------------------------
# howto C++ library: libgnuradio-howto.so
# ----------------------------------------------------------------

# C/C++ headers get installed in ${prefix}/include/$(modname)
modinclude_HEADERS = \
	howto_square_ff.h \
	howto_square2_ff.h \
	howto_detect_cut_vcc.h \
	howto_de_diff_mod_vcc.h \
	howto_de_freq_interleaver_vcf.h \
	howto_sub_channel_vff.h \
	howto_time_interleaving_vff.h \
	howto_depuncturing_vff.h \
	howto_energy_disp_vbb.h \
	howto_fib_crc16_vbb.h \
	howto_viterbi_vfb.h \
	howto_fib_sink_vb.h \
	howto_cutter_vbb.h \
	howto_bonder_vff.h \
	howto_framestart_detecter_cc.h \
	howto_ofdm_symbol_cutter_cc.h \
	howto_null_symbol_resample_bb.h \
	howto_interpolation_cc.h \
	howto_fib_sink2_vb.h \
	howto_prearrangement_vbb.h \
	howto_fib_sink3_vbf.h

lib_LTLIBRARIES = libgnuradio-howto.la

libgnuradio_howto_la_SOURCES = \
	howto_square_ff.cc \
	howto_square2_ff.cc \
	howto_detect_cut_vcc.cc \
	howto_de_diff_mod_vcc.cc \
	howto_de_freq_interleaver_vcf.cc \
	howto_sub_channel_vff.cc \
	howto_time_interleaving_vff.cc \
	howto_depuncturing_vff.cc \
	howto_energy_disp_vbb.cc \
	howto_fib_crc16_vbb.cc \
	howto_viterbi_vfb.cc \
	howto_fib_sink_vb.cc \
	howto_cutter_vbb.cc \
	howto_bonder_vff.cc \
	howto_framestart_detecter_cc.cc \
	howto_ofdm_symbol_cutter_cc.cc \
	howto_null_symbol_resample_bb.cc \
	howto_interpolation_cc.cc \
	howto_fib_sink2_vb.cc \
	howto_prearrangement_vbb.cc \
	howto_fib_sink3_vbf.cc

libgnuradio_howto_la_LIBADD = \
	$(GNURADIO_CORE_LA)

libgnuradio_howto_la_LDFLAGS = $(NO_UNDEFINED) $(LTVERSIONFLAGS)

# ----------------------------------------------------------------
# howto C++ QA library: libgnuradio-howto-qa.so (not installed)
# ----------------------------------------------------------------

noinst_LTLIBRARIES = libgnuradio-howto-qa.la

libgnuradio_howto_qa_la_SOURCES = \
	qa_howto.cc \
	qa_howto_square_ff.cc \
	qa_howto_square2_ff.cc \
	qa_howto_de_diff_mod_vcc.cc \
	qa_howto_de_freq_interleaver_vcf.cc \
	qa_howto_sub_channel_vff.cc \
	qa_howto_time_interleaving_vff.cc \
	qa_howto_depuncturing_vff.cc \
	qa_howto_energy_disp_vbb.cc \
	qa_howto_fib_crc16_vbb.cc \
	qa_howto_viterbi_vfb.cc \
	qa_howto_fib_sink_vb.cc \
	qa_howto_cutter_vbb.cc \
	qa_howto_bonder_vff.cc \
	qa_howto_framestart_detecter_cc.cc \
	qa_howto_ofdm_symbol_cutter_cc.cc \
	qa_howto_null_symbol_resample_bb.cc \
	qa_howto_interpolation_cc.cc \
	qa_howto_fib_sink2_vb.cc \
	qa_howto_prearrangement_vbb.cc \
	qa_howto_fib_sink3_vbf.cc

libgnuradio_howto_qa_la_LDFLAGS = $(NO_UNDEFINED) -version-info 0:0:0

libgnuradio_howto_qa_la_LIBADD = \
	libgnuradio-howto.la \
	$(CPPUNIT_LIBS)

# ----------------------------------------------------------------
# headers that don't get installed
# ----------------------------------------------------------------
noinst_HEADERS = \
	qa_howto.h \
	qa_howto_square_ff.h \
	qa_howto_square2_ff.h \
	qa_howto_de_diff_mod_vcc.h \
	qa_howto_de_freq_interleaver_vcf.h \
	qa_howto_sub_channel_vff.h \
	qa_howto_time_interleaving_vff.h \
	qa_howto_depuncturing_vff.h \
	qa_howto_energy_disp_vbb.h \
	qa_howto_fib_crc16_vbb.h \
	qa_howto_viterbi_vfb.h \
	qa_howto_fib_sink_vb.h \
	qa_howto_cutter_vbb.h \
	qa_howto_bonder_vff.h \
	qa_howto_framestart_detecter_cc.h \
	qa_howto_ofdm_symbol_cutter_cc.h \
	qa_howto_null_symbol_resample_bb.h \
	qa_howto_interpolation_cc.h \
	qa_howto_fib_sink2_vb.h \
	qa_howto_prearrangement_vbb.h \
	qa_howto_fib_sink3_vbf.h

# ----------------------------------------------------------------
# test program
# ----------------------------------------------------------------
noinst_PROGRAMS = \
	test_all

test_all_SOURCES = test_all.cc
test_all_LDADD   = libgnuradio-howto-qa.la
