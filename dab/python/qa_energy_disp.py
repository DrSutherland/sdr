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

    def test_001_energy_disp_vbb (self):
        #################################
        # Testsequenz generieren
        src_data_1 = []
        for number in range(22):
            src_data_1.append(0)
        for number in range(22):
            src_data_1.append(1)
        
        src_data_0 = []
        src_data_0.extend(src_data_1)
        for number in range(200):
            src_data_0.extend(src_data_1)
                
        ################################
        # Ergebnis generieren
        expected_result_1 = (0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,0,
                             1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1)
        expected_result_2 = list()
        expected_result_2.extend(expected_result_1)
        
        for number in range(200):
            expected_result_2.extend(expected_result_1)
        
        expected_result_0 = tuple(expected_result_2)
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_b (src_data_0)
        throttle_0 = gr.throttle(gr.sizeof_char*1, 320000)
        s2v_0 = gr.stream_to_vector(gr.sizeof_char, 22)
        Energy_disp = howto_swig.energy_disp_vbb(22)
        v2s_0 = gr.vector_to_stream(gr.sizeof_char, 16)
        dst_0 = gr.vector_sink_b()
        
        # Objekte verbinden
        self.tb.connect(src_0, throttle_0, s2v_0,Energy_disp,v2s_0,dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertEqual(expected_result_0, result_data0)
        
    def test_002_energy_disp_vbb (self):
        #################################
        src_data_0 = []
        for number in range(22):
            src_data_0.append(0)
        for number in range(22):
            src_data_0.append(1)
                
        ################################
        expected_result_0 = (0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,0,
                             1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1)
        
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_b (src_data_0)
        s2v_0 = gr.stream_to_vector(gr.sizeof_char, 22)
        Energy_disp = howto_swig.energy_disp_vbb(22)
        v2s_0 = gr.vector_to_stream(gr.sizeof_char, 16)
        dst_0 = gr.vector_sink_b()
        
        # Objekte verbinden
        self.tb.connect(src_0, s2v_0,Energy_disp,v2s_0,dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertEqual(expected_result_0, result_data0)
        
if __name__ == '__main__':
    gr_unittest.main ()
