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

    def test_006_sub_channel_vff (self):
        #################################
        # Testsequenz generieren
        
        src_data_0 = []
        for number in range(76*3072):       #0=Sync,1-3=FIC,4-75  -> Sum = 76 Symbole
            if number == 1*3072:
                src_data_0.append(2)         #FIB1 Anfang	(Checked)
            elif number == 1*3072+2303:
                src_data_0.append(3)         #FIB1 Ende		(Checked)
            elif number == 4*3072-1:
                src_data_0.append(4)         #FIB4 Ende		(Checked)
            elif number == 4*3072+64*188:
                src_data_0.append(5)         #Subchannel Start CIF1 (Adr 188)	(Checked)
            elif number == 4*3072+64*(188+84)-1:
                src_data_0.append(6)         #Subchannel Ende CIF1 (Size 84)	(Checked)
            elif number == 4*3072+64*188+55296:
                src_data_0.append(7)         #Subchannel Start CIF2 (Size 84)	(Checked)
            elif number == 4*3072+64*(188+84)-1+55296:
                src_data_0.append(8)         #Subchannel Ende CIF2 (Size 84)	(Checked)
            else:
                src_data_0.append(0)
                
        src_data_1 = []
        for number in range(76):
            if (number%76) == 0:
                src_data_1.append(1)         # Frame Startflag
            else:
                src_data_1.append(0)
        ################################
        # Ergebnis generieren
        
        expected_result_0 = []               # SubChannel Test
        for number in range(4*(84*64)):
            if number == 0:
                expected_result_0.append(5)
            elif number == 1*84*64-1:
                expected_result_0.append(6)
            elif number == 1*84*64:
                expected_result_0.append(7)
            elif number == 2*84*64-1:
                expected_result_0.append(8)
            else:
                expected_result_0.append(0)
        
        expected_result_1 = []               # FIB Test
        for number in range(4*2304):
            if number == 0:
                expected_result_1.append(2)
            elif number == 1*2304-1:
                expected_result_1.append(3)
            elif number == 4*2304-1:
                expected_result_1.append(4)
            else:
                expected_result_1.append(0)
        #################################
        
        # Objekte erzeugen
        src1 = gr.vector_source_f (src_data_0)
        throttle_0 = gr.throttle(gr.sizeof_float*1, 320000)
        s2v = gr.stream_to_vector(gr.sizeof_float, 3072)
        src2 = gr.vector_source_b (src_data_1)
        SubCha = howto_swig.sub_channel_vff(3072/2,188,84)
        v2s_0 = gr.vector_to_stream(gr.sizeof_float, 84*64/8)
        v2s_1 = gr.vector_to_stream(gr.sizeof_float, 2304/8)
        dst0 = gr.vector_sink_f()
        dst1 = gr.vector_sink_f()
        
        # Objekte verbinden
        self.tb.connect(src1,throttle_0, s2v, (SubCha,0))
        self.tb.connect(src2, (SubCha,1))
        self.tb.connect((SubCha,0),v2s_0,dst0)
        self.tb.connect((SubCha,1),v2s_1,dst1)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst0.data ()
        self.assertFloatTuplesAlmostEqual (expected_result_0, result_data0, 6)
        result_data1 = dst1.data ()
        self.assertFloatTuplesAlmostEqual (expected_result_1, result_data1, 6)
        
        
        
        
if __name__ == '__main__':
    gr_unittest.main ()
