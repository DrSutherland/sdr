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

// WARNING: this file is machine generated.  Edits will be over written

 // Zürcher Hochschule für Angewandte Wissenschaften
 // Zentrum für Signalverarbeitung und Nachrichtentechnik
 // Michael Höin, 2011
 // info.zsn@zhaw.ch

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>

#include <howto_ofdm_symbol_cutter_cc.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of ofdm_symbol_cutter_cc and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_ofdm_symbol_cutter_cc_sptr 
 howto_make_ofdm_symbol_cutter_cc(unsigned int tf,
                           unsigned int tu,
                           unsigned int delta,
                           unsigned int l,
                           unsigned int offset)
{
  return howto_ofdm_symbol_cutter_cc_sptr (new howto_ofdm_symbol_cutter_cc (tf,tu, delta, l, offset));
}

/*
 * The private constructor
 */
howto_ofdm_symbol_cutter_cc::howto_ofdm_symbol_cutter_cc (unsigned int tf,
                                            unsigned int tu,
                                            unsigned int delta,
                                            unsigned int l,
                                            unsigned int offset)
  : gr_block ("ofdm_symbol_cutter_cc",
		   gr_make_io_signature2 (2, 2, sizeof (gr_complex),sizeof (char)),
		   gr_make_io_signature2 (2, 2, sizeof (gr_complex),sizeof (char))),
		   d_tf(tf),				// Framelength (Standard EN 300 401 Page 145)
		   d_tu(tu), 				// FFT length (Standard EN 300 401 Page 145)
		   d_delta(delta), 			// GardTime (Standard EN 300 401 Page 145)
		   d_l(l), 					// Nbr of Symbols (Standard EN 300 401 Page 145)
		   d_counter_sample(0),		// Samplecounter
		   d_counter_symbol(0),		// Symbolcounter
		   d_state(STATE_Detect), 	// Start State
		   d_offset(offset)			// Time between detection and first symbol
{
  set_relative_rate((double)(tu*l)/(double)tf);		// In one frame (tf complex values) we produce tu*l complex values
}

void
howto_ofdm_symbol_cutter_cc::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = d_tf/(d_tu*d_l);		// Average used complex values on the input
}

howto_ofdm_symbol_cutter_cc::~howto_ofdm_symbol_cutter_cc ()
{
  	
}

int
howto_ofdm_symbol_cutter_cc::general_work (int noutput_items,
			                        gr_vector_int &ninput_items,
			                        gr_vector_const_void_star &input_items,
			                        gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];
	const char *in2 = (const char *) input_items[1];
	gr_complex *out = (gr_complex *) output_items[0];
	char *out2 = (char *) output_items[1];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples Port1
	unsigned int input_samples2 = ninput_items[1];	// Nbr Inputsamples Port2
	unsigned int input_used = 0;					// Used inputs
	unsigned int output_generated_counter = 0;		// Produced outputs
	
//------------------------------------------------------------------------------------------
	while (input_used < input_samples && input_used < input_samples2 && output_generated_counter< noutput_items)
	{
		switch (d_state) {
			//------------------------------------------------------------------------------------------
			// Check if the framestart occurre
			case(STATE_Detect):
				if(in2[0]==1)
					d_state = STATE_Offset;
					d_counter_sample = 0;
				break;
			//------------------------------------------------------------------------------------------
			// Elapse the time until the first symbol
			case(STATE_Offset):
				if(d_counter_sample < d_offset-1) d_counter_sample++;
				else 
				{	
					d_state = STATE_Symbol;
					d_counter_sample = 0;
				}
				break;
			//------------------------------------------------------------------------------------------
			// Symboldata transfer
			case(STATE_Symbol):
			
				if(d_counter_sample < d_tu)
				{
					out[0]=in[0];
					out++;
					out2[0]= (d_counter_symbol == 0 && d_counter_sample == 0)? 1: 0;
					out2++;
					output_generated_counter++;
					d_counter_sample++;
				}
				else 									// A entire symbol was transfered
				{
					d_counter_sample = 0;
					if (d_counter_symbol == d_l-1)		// last symbol in frame?
					{
						d_state = STATE_Detect;			// change to detection state
						d_counter_symbol=0;				// reset symbolcounter
					}
					else
					{
						d_state = STATE_GuardTime;		// It follows a guard time
						d_counter_symbol++;
					}
				}
				
				break;
			//------------------------------------------------------------------------------------------
			// Elaps the guard time between two symbols
			case(STATE_GuardTime):
				if(d_counter_sample < d_delta-2) d_counter_sample++;
					else 
				{
					d_state = STATE_Symbol;
					d_counter_sample = 0;
				}
				break;
			//------------------------------------------------------------------------------------------
		}
		
		in++;
		in2++;
		input_used++;
	}
	
	consume_each(input_used);						// Inputvalues used
	return output_generated_counter;				// Generated values
}
