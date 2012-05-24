/* -*- c++ -*- */
/*
 * Copyright 2004,2010 Free Software Foundation, Inc.
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
 
 // Zürcher Hochschule für Angewandte Wissenschaften
 // Zentrum für Signalverarbeitung und Nachrichtentechnik
 // Michael Höin, 2011
 // info.zsn@zhaw.ch


#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>

#include <howto_de_diff_mod_vcc.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of howto_de_diff_mod_vcc and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_de_diff_mod_vcc_sptr 
 howto_make_de_diff_mod_vcc(unsigned int tu, unsigned int extract)
{
  return howto_de_diff_mod_vcc_sptr (new howto_de_diff_mod_vcc (tu,extract));
}

/*
 * The private constructor
 */
howto_de_diff_mod_vcc::howto_de_diff_mod_vcc (unsigned int tu, unsigned int extract)
  : gr_sync_block ("de_diff_mod_vcc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)*tu),
		   gr_make_io_signature2 (1, 2, sizeof (gr_complex)*tu, sizeof (gr_complex))),
		   d_tu(tu), 				// FFT laenge (Standard EN 300 401 Page 145)
		   d_extract(extract)		// Welcher Subcarrierer soll zum Darstellen ausgegeben werden
{
  set_history(2);
}

/*
 * Our virtual destructor.
 */
howto_de_diff_mod_vcc::~howto_de_diff_mod_vcc ()
{
  // nothing else required in this example
}

/* adapted from dab_diff_phasor_vcc.cc (Andreas Mueller)*/

int 
howto_de_diff_mod_vcc::work (int noutput_items,
							 gr_vector_const_void_star &input_items,
							 gr_vector_void_star &output_items)
{
  const gr_complex *in = (const gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];
  gr_complex *out2 = (gr_complex *) output_items[1];
  
  unsigned int extract_counter = 0;
  
  for(unsigned int i = 0; i < noutput_items*d_tu; i++){
	//------------------------------------------------------------------------------------------
	// Differentielle Modulation rückgängig machen
    out[i] = in[i+d_tu] * conj(in[i]);
    
    //------------------------------------------------------------------------------------------
    // Ein Sample extrahieren um die Modulation Plotten zu können
    if (d_extract == 0)
    {
        out2[extract_counter] = out[i];
        extract_counter ++;
        d_extract = d_tu-1;
	}
	else
	{
		d_extract --;
	}
    
  }
    
  return noutput_items;
}
