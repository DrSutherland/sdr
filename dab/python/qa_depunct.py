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

    def test_008_depuncturing_vff (self):
        #################################
        # Testsequenz generieren
        src_data_0 = []
        for number in range(256+1):  #+1 Da null wegfaellt
            if number != 0:
                src_data_0.append((number%100))
                
        ################################
        # Ergebnis generieren
        expected_result_0 = [ 1, 2, 0, 0,  3, 0, 0, 0,  4, 0, 0, 0,  5, 0, 0, 0,  6, 7, 0, 0,  8, 0, 0, 0,  9, 0, 0, 0, 10, 0, 0, 0,  #PI2
                             11,12, 0, 0, 13, 0, 0, 0, 14, 0, 0, 0, 15, 0, 0, 0, 16,17, 0, 0, 18, 0, 0, 0, 19, 0, 0, 0, 20, 0, 0, 0,  #PI2
                             21,22, 0, 0, 23, 0, 0, 0, 24, 0, 0, 0, 25, 0, 0, 0, 26,27, 0, 0, 28, 0, 0, 0, 29, 0, 0, 0, 30, 0, 0, 0,  #PI2
                             31,32, 0, 0, 33, 0, 0, 0, 34, 0, 0, 0, 35, 0, 0, 0, 36,37, 0, 0, 38, 0, 0, 0, 39, 0, 0, 0, 40, 0, 0, 0,  #PI2
                             #
                             41,42, 0, 0, 43,44, 0, 0, 45,46, 0, 0, 47,48, 0, 0, 49,50, 0, 0, 51,52, 0, 0, 53,54, 0, 0, 55,56, 0, 0,  #PI8
                             57,58, 0, 0, 59,60, 0, 0, 61,62, 0, 0, 63,64, 0, 0, 65,66, 0, 0, 67,68, 0, 0, 69,70, 0, 0, 71,72, 0, 0,  #PI8
                             73,74, 0, 0, 75,76, 0, 0, 77,78, 0, 0, 79,80, 0, 0, 81,82, 0, 0, 83,84, 0, 0, 85,86, 0, 0, 87,88, 0, 0,  #PI8
                             89,90, 0, 0, 91,92, 0, 0, 93,94, 0, 0, 95,96, 0, 0, 97,98, 0, 0, 99, 0, 0, 0,  1, 2, 0, 0,  3, 4, 0, 0,  #PI8
                             #
                              5, 6, 7, 0,  8, 9,10, 0, 11,12,13, 0, 14,15,16, 0, 17,18,19, 0, 20,21,22, 0, 23,24,25, 0, 26,27, 0, 0,  #PI15
                             28,29,30, 0, 31,32,33, 0, 34,35,36, 0, 37,38,39, 0, 40,41,42, 0, 43,44,45, 0, 46,47,48, 0, 49,50, 0, 0,  #PI15
                             51,52,53, 0, 54,55,56, 0, 57,58,59, 0, 60,61,62, 0, 63,64,65, 0, 66,67,68, 0, 69,70,71, 0, 72,73, 0, 0,  #PI15
                             74,75,76, 0, 77,78,79, 0, 80,81,82, 0, 83,84,85, 0, 86,87,88, 0, 89,90,91, 0, 92,93,94, 0, 95,96, 0, 0,  #PI15
                             #
                             97,98, 0, 0, 99, 0, 0, 0,  0, 1, 0, 0,  2, 0, 0, 0,  3, 4, 0, 0,  5, 0, 0, 0,  6, 7, 0, 0,  8, 0, 0, 0,  #PI4
                              9,10, 0, 0, 11, 0, 0, 0, 12,13, 0, 0, 14, 0, 0, 0, 15,16, 0, 0, 17, 0, 0, 0, 18,19, 0, 0, 20, 0, 0, 0,  #PI4
                             21,22, 0, 0, 23, 0, 0, 0, 24,25, 0, 0, 26, 0, 0, 0, 27,28, 0, 0, 29, 0, 0, 0, 30,31, 0, 0, 32, 0, 0, 0,  #PI4
                             33,34, 0, 0, 35, 0, 0, 0, 36,37, 0, 0, 38, 0, 0, 0, 39,40, 0, 0, 41, 0, 0, 0, 42,43, 0, 0, 44, 0, 0, 0,  #PI4
                             #
                             45,46, 0, 0, 47,48, 0, 0, 49,50, 0, 0, 51,52, 0, 0, 53,54, 0, 0, 55,56, 0, 0, #Tail
                            ]
        
        #################################
        
        # Objekte erzeugen
        src_0 = gr.vector_source_f (src_data_0)
        s2v_0 = gr.stream_to_vector(gr.sizeof_float, 4*64)
        Depunct = howto_swig.depuncturing_vff(4,2,1,8,1,15,1,4,1)       # PI=2,8,15,4
        v2s_0 = gr.vector_to_stream(gr.sizeof_float, (1+1+1+1)*32*4+24)
        dst_0 = gr.vector_sink_f()
        
        # Objekte verbinden
        self.tb.connect(src_0, s2v_0,Depunct,v2s_0,dst_0)
        
        # Simulationsstart
        self.tb.run ()
        
        # Ergebnis auswerten
        result_data0 = dst_0.data ()
        self.assertFloatTuplesAlmostEqual (expected_result_0, result_data0, 6)
        
        
        
if __name__ == '__main__':
    gr_unittest.main ()
