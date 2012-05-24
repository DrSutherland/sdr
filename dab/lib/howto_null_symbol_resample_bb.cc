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

#include <howto_null_symbol_resample_bb.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of null_symbol_resample_bb and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_null_symbol_resample_bb_sptr 
 howto_make_null_symbol_resample_bb(unsigned int tu)
{
  return howto_null_symbol_resample_bb_sptr (new howto_null_symbol_resample_bb (tu));
}

/*
 * The private constructor
 */
howto_null_symbol_resample_bb::howto_null_symbol_resample_bb (unsigned int tu)
  : gr_block ("null_symbol_resample_bb",
		   gr_make_io_signature (1, 1, sizeof (char)),
		   gr_make_io_signature (1, 1, sizeof (char))),
		   d_tu(tu), 				// FFT laenge (Standard EN 300 401 Page 145)
		   d_counter_sample(0)		// Zaehlvariable der Samples in den Frame Abschnitten
{
  set_relative_rate((double)(1)/(double)tu);
}

void
howto_null_symbol_resample_bb::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = d_tu;		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
}

howto_null_symbol_resample_bb::~howto_null_symbol_resample_bb ()
{
  	
}

int
howto_null_symbol_resample_bb::general_work (int noutput_items,
			                        gr_vector_int &ninput_items,
			                        gr_vector_const_void_star &input_items,
			                        gr_vector_void_star &output_items)
{
	const char *in = (const char *) input_items[0];
	char *out = (char *) output_items[0];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples
	unsigned int input_used = 0;					// Index Inputvektor
	unsigned int output_generated_counter = 0;		// Anzahl generierte Outputvektoren
	
//------------------------------------------------------------------------------------------
	while (input_used < input_samples && output_generated_counter<noutput_items)
	{
		if (d_counter_sample==d_tu) d_counter_sample = 0;	// Verarbeitete Samples in einem Frame zaehlen
		
		if (d_counter_sample==0) 							// Nur erstes Sample eines Symbols beachten
		{
			out[0]=in[0];
			out++;
			output_generated_counter++;
		}
		
		d_counter_sample++;
		
		in++;
		input_used++;
	}
	
	consume_each(input_used);						// Wieviel vom Inputvektor gebruacht wurde
	return output_generated_counter;							// Anzahl Outputdaten
}
