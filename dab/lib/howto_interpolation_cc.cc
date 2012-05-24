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

#include <howto_interpolation_cc.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of interpolation_cc and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_interpolation_cc_sptr 
 howto_make_interpolation_cc(unsigned int interpolation,
                           unsigned int decimation)
{
  return howto_interpolation_cc_sptr (new howto_interpolation_cc (interpolation, decimation));
}

/*
 * The private constructor
 */
howto_interpolation_cc::howto_interpolation_cc (unsigned int interpolation,
                                            unsigned int decimation)
  : gr_block ("interpolation_cc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)),
		   gr_make_io_signature (1, 1, sizeof (gr_complex))),
		   d_interpolation(interpolation),						// Interpolationsfaktor
		   d_decimation(decimation),							// Dezimationsfaktor
		   d_counter(0)											// Zaehlvariable zum einwandfreinen verarbeiten von mehreren Datenbloecken
{
  set_history(2);
  set_relative_rate((double)(interpolation)/(double)(decimation)+1);		// In one frame (tf complex values) we produce tu*l complex values
}

void
howto_interpolation_cc::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = d_interpolation/d_decimation+1;		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
}

howto_interpolation_cc::~howto_interpolation_cc ()
{
  
}

int
howto_interpolation_cc::general_work (int noutput_items,
			                        gr_vector_int &ninput_items,
			                        gr_vector_const_void_star &input_items,
			                        gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];		// (Input) Datenvektor
  
	gr_complex *out = (gr_complex *) output_items[0];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples
	unsigned int input_used = 0;					// Index Inputvektor
	unsigned int output_generated_counter = 0;		// Anzahl generierte Outputvektoren
	float MemReal;
	float MemImag;
	
//------------------------------------------------------------------------------------------
	
	while (input_used < input_samples)
	{
		//--------------------------------------------------------------------------------------
		while(d_counter<d_interpolation)										// Alle Werte zwischen zwei Werten generieren
		{
			
			MemReal = (in[1].real()-in[0].real())*d_counter/d_interpolation;	// Lineare Interpolation I Kanal
			MemReal+= in[0].real();
			
			MemImag = (in[1].imag()-in[0].imag())*d_counter/d_interpolation;	// Lineare Interpolation Q Kanal
			MemImag+= in[0].imag();
			
			out[0]= gr_complex (MemReal, MemImag);
			out++;
			output_generated_counter++;
			
			d_counter+=d_decimation;
		}
		
		d_counter %= d_interpolation;
		in++;
		input_used++;
	}
	
	consume_each(input_used);						// Wieviel vom Inputvektor gebruacht wurde
	return output_generated_counter;							// Anzahl Outputdaten
}
