#!/usr/bin/env python
#
# Copyright 2004,2007 Free Software Foundation, Inc.
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

from gnuradio import gr, gr_unittest
from gnuradio import trellis
import howto_swig

class qa_howto (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_003_ofdm_symbol_cutter_cc (self):
        #################################
        # Testsequenz generieren
        src_data_0 = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
        src_data_1 = [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
                
        ################################
        # Ergebnis generieren
        exp_resu_0 = [             5, 6, 7,      10,11,12,         16,17,18,      21,22,23,            28,29,30,      33]
        exp_resu_1 = (             1, 0, 0,       0, 0, 0,          1, 0, 0,       0, 0, 0,             1, 0, 0,       0)
        
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_c (src_data_0)
        src_1 = gr.vector_source_b (src_data_1)
        throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, 320000)
        throttle_1 = gr.throttle(gr.sizeof_char*1, 320000)
        ofdm_symbole = howto_swig.ofdm_symbol_cutter_cc(11,3,2,2,1)		#Blockgroesse=3, Guardtime = 1, Blockanzahl=2, Offset=1
        dst_0 = gr.vector_sink_c()
        dst_1 = gr.vector_sink_b()
        
        # Objekte verbinden
        self.tb.connect(src_0, throttle_0, (ofdm_symbole,0))
        self.tb.connect(src_1, throttle_1, (ofdm_symbole,1))
        self.tb.connect((ofdm_symbole,0), dst_0)
        self.tb.connect((ofdm_symbole,1), dst_1)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        result_data1 = dst_1.data ()
        self.assertComplexTuplesAlmostEqual (exp_resu_0, result_data0, 6)
        self.assertEqual(exp_resu_1, result_data1)
        
    def test_002null_symbol_resample_bb (self):
        #################################
        # Testsequenz generieren
        src_data_0 = (1, 0, 0,       0, 0, 0,          1, 0, 0,       0, 0, 0,             1, 0, 0,       0)
                
        ################################
        # Ergebnis generieren
        exp_resu_0 = (1,             0,                1,             0,                   1,             0)
        
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_b (src_data_0)
        throttle_0 = gr.throttle(gr.sizeof_char*1, 320000)
        null_symbol_resample = howto_swig.null_symbol_resample_bb(3)		#Blockgroesse=3, Guardtime = 1, Blockanzahl=2, Offset=1
        dst_0 = gr.vector_sink_b()
        
        # Objekte verbinden
        self.tb.connect(src_0, throttle_0, (null_symbol_resample,0))
        self.tb.connect((null_symbol_resample,0), dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertEqual(exp_resu_0, result_data0)
        
        
if __name__ == '__main__':
    gr_unittest.main ()
