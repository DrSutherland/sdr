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

    def test_005_de_freq_interleaver_vcf (self):
        #################################
        # Testsequenz generieren
        src_data = []
        for number in range(2048):
            if number == 511:
                src_data.append(1+2j)
            else:
                src_data.append(0+0j)
        for number in range(2048):
            if number == 511:
                src_data.append(1+2j)
            else:
                src_data.append(0+0j)
        
        #################################
        # Ergebnis generieren
        expected_result_0 = []
        for number in range(1536*2):
            if number == 0:
                expected_result_0.append(1)
            elif number == 1536:
                expected_result_0.append(2)
            else:
                expected_result_0.append(0)
        for number in range(1536*2):
            if number == 0:
                expected_result_0.append(1)
            elif number == 1536:
                expected_result_0.append(2)
            else:
                expected_result_0.append(0)
        #################################
        
        # Objekte erzeugen
        src = gr.vector_source_c (src_data)
        s2v = gr.stream_to_vector(gr.sizeof_gr_complex, 2048)
        interl = howto_swig.de_freq_interleaver_vcf(2048,1536)
        v2s = gr.vector_to_stream(gr.sizeof_float, 1536*2)
        dst0 = gr.vector_sink_f()
        
        # Objekte verbinden
        self.tb.connect(src, s2v, interl, v2s, dst0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst0.data ()
        self.assertFloatTuplesAlmostEqual (expected_result_0, result_data0, 6)
        
        
        
if __name__ == '__main__':
    gr_unittest.main ()
