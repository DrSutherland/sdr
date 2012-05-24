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

    def test_001_interpolation_cc (self):
        #################################
        # Testsequenz generieren
        src_data_0 = (         3+0j,    6+0j,          6+6j,    6+6j,          0+0j,     3+3j)
                
        ################################
        # Ergebnis generieren
        exp_resu_0 = (   0+0j, 2+0j,    4+0j,    6+0j, 6+4j,    6+6j,    6+6j, 2+2j,     1+1j,   3+3j,1+1j)
        
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_c (src_data_0)
        throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, 320000)
        interpol = howto_swig.interpolation_cc(3,2)
        dst_0 = gr.vector_sink_c()
        
        # Objekte verbinden
        self.tb.connect(src_0, throttle_0)
        self.tb.connect(throttle_0, interpol)
        self.tb.connect(interpol, dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertComplexTuplesAlmostEqual (exp_resu_0, result_data0, 6)
        
if __name__ == '__main__':
    gr_unittest.main ()
