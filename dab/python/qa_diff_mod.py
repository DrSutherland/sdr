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
        
    def test_003_de_diff_mod_vcc (self):
        #################################
        # Testsequenz generieren
        src_data =        (1+0j, 0+2j, 0-0j, 0+1j, 2+0j, 0+0j,-1+0j,2+0j,-0+0j)
        #################################
        # Ergebnis generieren
        expected_result_0 = (0+0j, 0+0j, 0-0j, 0+1j, 0-4j, 0-0j, 0+1j, 4+0j, 0+0j)
        expected_result_1 = (0+0j, 0+1j, 0+1j)
        #################################
        
        # Objekte erzeugen
        src = gr.vector_source_c (src_data)
        s2v = gr.stream_to_vector(gr.sizeof_gr_complex, 3)
        diff = howto_swig.de_diff_mod_vcc(3,0)
        v2s = gr.vector_to_stream(gr.sizeof_gr_complex, 3)
        dst0 = gr.vector_sink_c()
        dst1 = gr.vector_sink_c()
        
        # Objekte verbinden
        self.tb.connect(src, s2v, (diff,0), v2s, dst0)
        self.tb.connect((diff,1), dst1)
        
        # Simulationsstart
        self.tb.run ()
        result_data0 = dst0.data ()
        result_data1 = dst1.data ()
        self.assertComplexTuplesAlmostEqual (expected_result_0, result_data0, 6)
        self.assertComplexTuplesAlmostEqual (expected_result_1, result_data1, 6)
        
    def test_004_de_diff_mod_vcc (self):
        #################################
        # Testsequenz generieren
        src_data =        (1+0j, 0+2j, 0-0j, 0+1j, 2+0j, 0+0j,-1+0j,2+0j,-0+0j)
        #################################
        # Ergebnis generieren
        expected_result_0 = (0+0j, 0+0j, 0-0j, 0+1j, 0-4j, 0-0j, 0+1j, 4+0j, 0+0j)
        expected_result_1 = (0+0j, 0-4j, 4+0j)
        #################################
        
        # Objekte erzeugen
        src = gr.vector_source_c (src_data)
        s2v = gr.stream_to_vector(gr.sizeof_gr_complex, 3)
        diff = howto_swig.de_diff_mod_vcc(3,1)
        v2s = gr.vector_to_stream(gr.sizeof_gr_complex, 3)
        dst0 = gr.vector_sink_c()
        dst1 = gr.vector_sink_c()
        
        # Objekte verbinden
        self.tb.connect(src, s2v, (diff,0), v2s, dst0)
        self.tb.connect((diff,1), dst1)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst0.data ()
        result_data1 = dst1.data ()
        self.assertComplexTuplesAlmostEqual (expected_result_0, result_data0, 6)
        self.assertComplexTuplesAlmostEqual (expected_result_1, result_data1, 6)
        
        
if __name__ == '__main__':
    gr_unittest.main ()
