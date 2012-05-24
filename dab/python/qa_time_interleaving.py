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

    def test_007_time_interleaving_vff (self):
        #################################
        # Testsequenz generieren
        
        src_data_0 = []
        #1CIF, 84CU,64Bit (Data)
        for number in range(1*84*64):
            src_data_0.append((number%16))
            
        #15CIF, 84CU,64Bit (Blank)
        for number in range(15*84*64):
            src_data_0.append(0)
        ################################
        # Ergebnis generieren
        expected_result_0 = []
        
        #Bit-Delays in the Receiver (Unit CIFs)--> (Bitposition Mod 16)
        interleavingOrder = [15,7,11,3,13,5,9,1,14,6,10,2,12,4,8,0]
        
        for CIF in range(16):
          interleavingValue = interleavingOrder[CIF]
          for number in range(1*84*64):
            if (number%16) == interleavingValue:
               expected_result_0.append(interleavingValue)
            else: 
               expected_result_0.append(0)
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_f (src_data_0)
        throttle_0 = gr.throttle(gr.sizeof_float*1, 320000)
        s2v_0 = gr.stream_to_vector(gr.sizeof_float, 84*64/8)
        TimeInt = howto_swig.time_interleaving_vff(84)
        v2s_0 = gr.vector_to_stream(gr.sizeof_float, 84*64)
        dst_0 = gr.vector_sink_f()
        
        # Objekte verbinden
        self.tb.connect(src_0, throttle_0, s2v_0,TimeInt,v2s_0,dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertFloatTuplesAlmostEqual (expected_result_0, result_data0, 6)
        
        
        
if __name__ == '__main__':
    gr_unittest.main ()
