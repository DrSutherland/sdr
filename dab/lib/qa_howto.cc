/*
 * Copyright 2009 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

/*
 * This class gathers together all the test cases for the example
 * directory into a single test suite.  As you create new test cases,
 * add them here.
 */

#include <qa_howto.h>
#include <qa_howto_square_ff.h>
#include <qa_howto_square2_ff.h>
#include <qa_howto_de_diff_mod_vcc.h>
#include <qa_howto_de_freq_interleaver_vcf.h>
#include <qa_howto_depuncturing_vff.h>
#include <qa_howto_sub_channel_vff.h>
#include <qa_howto_time_interleaving_vff.h>
#include <qa_howto_energy_disp_vbb.h>
#include <qa_howto_fib_crc16_vbb.h>
#include <qa_howto_viterbi_vfb.h>
#include <qa_howto_fib_sink_vb.h>
#include <qa_howto_cutter_vbb.h>
#include <qa_howto_bonder_vff.h>
#include <qa_howto_framestart_detecter_cc.h>
#include <qa_howto_ofdm_symbol_cutter_cc.h>
#include <qa_howto_null_symbol_resample_bb.h>
#include <qa_howto_interpolation_cc.h>
#include <qa_howto_fib_sink2_vb.h>
#include <qa_howto_prearrangement_vbb.h>
#include <qa_howto_fib_sink3_vbf.h>

CppUnit::TestSuite *
qa_howto::suite()
{
  CppUnit::TestSuite *s = new CppUnit::TestSuite("howto");

  s->addTest(qa_howto_square_ff::suite());
  s->addTest(qa_howto_square2_ff::suite());
  s->addTest(qa_howto_de_diff_mod_vcc::suite());
  s->addTest(qa_howto_de_freq_interleaver_vcf::suite());
  s->addTest(qa_howto_depuncturing_vff::suite());
  s->addTest(qa_howto_sub_channel_vff::suite());
  s->addTest(qa_howto_time_interleaving_vff::suite());
  s->addTest(qa_howto_energy_disp_vbb::suite());
  s->addTest(qa_howto_fib_crc16_vbb::suite());
  s->addTest(qa_howto_viterbi_vfb::suite());
  s->addTest(qa_howto_fib_sink_vb::suite());
  s->addTest(qa_howto_cutter_vbb::suite());
  s->addTest(qa_howto_bonder_vff::suite());
  s->addTest(qa_howto_framestart_detecter_cc::suite());
  s->addTest(qa_howto_ofdm_symbol_cutter_cc::suite());
  s->addTest(qa_howto_null_symbol_resample_bb::suite());
  s->addTest(qa_howto_interpolation_cc::suite());
  s->addTest(qa_howto_fib_sink2_vb::suite());
  s->addTest(qa_howto_prearrangement_vbb::suite());
  s->addTest(qa_howto_fib_sink3_vbf::suite());

  return s;
}
