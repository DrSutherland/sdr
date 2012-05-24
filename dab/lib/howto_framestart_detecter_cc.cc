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

#include <howto_framestart_detecter_cc.h>
#include <gr_io_signature.h>

// Michael Hoein, 2011

/*
 * Create a new instance of framestart_detecter_cc and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_framestart_detecter_cc_sptr 
 howto_make_framestart_detecter_cc(unsigned int tu,
                           unsigned int delta,
                           unsigned int l)
{
  return howto_framestart_detecter_cc_sptr (new howto_framestart_detecter_cc (tu, delta, l));
}

/*
 * The private constructor
 */
howto_framestart_detecter_cc::howto_framestart_detecter_cc (unsigned int tu,
                                            unsigned int delta,
                                            unsigned int l)
  : gr_block ("framestart_detecter_cc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)),
		   gr_make_io_signature (1, 1, sizeof (char))),
		   d_tu(tu), 				// FFT laenge (Standard EN 300 401 Page 145)
		   d_delta(delta), 			// GardTime (Standard EN 300 401 Page 145)
		   d_l(l), 					// Nbr of Symbols (Standard EN 300 401 Page 145)
		   d_counter(0), 			// Sample counter
		   d_rssi(1000),			// RSSI Start Value
		   d_pointer(0),			// Pointer in the RSSI-Ring-Memory
		   d_detect_delay(128),		// RSSI delay time
		   d_Data_Samples(0)		// Samples in a OFDM Frame
{
  d_array_delay = new float[d_detect_delay];
  int n;
  for (n=0; n<d_detect_delay; n++)
  {
	  d_array_delay [n] = 1000;
  }
  d_Data_Samples = d_l*(d_delta+d_tu);				// Samples in a OFDM Frame
}

void
howto_framestart_detecter_cc::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = 1;			// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
}

howto_framestart_detecter_cc::~howto_framestart_detecter_cc ()
{
  	delete [] d_array_delay;
}

int
howto_framestart_detecter_cc::general_work (int noutput_items,
			                        gr_vector_int &ninput_items,
			                        gr_vector_const_void_star &input_items,
			                        gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];
  
	char *out = (char *) output_items[0];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples available
	unsigned int input_used = 0;					// Inputs used
	unsigned int output_generated_counter = 0;		// Generated Outputvectors
	
//------------------------------------------------------------------------------------------

	float ampl_input;									// Absolutwert eines komplexen Inputsamples
	float abs_real;										// Betrag des Realanteils
	float abs_imag;										// Betrag des Imaginaeranteils
	const unsigned int forgetting = 3;					// Vergessensfaktor
	
	//------------------------------------------------------------------------------------------
	
	while (input_used < input_samples && output_generated_counter<noutput_items)
	{
		//--------------------------------------------------------------------------------------
		// Moving Average Filter calculate (RSSI)
		abs_real = (in[0].real() > 0) ? 
				   (in[0].real()) : 
				   (-in[0].real());		// ABS Real value
				   
		abs_imag = (in[0].imag() > 0) ? 
				   (in[0].imag()) : 
				   (-in[0].imag());		// ABS Imag value
		
		ampl_input = (abs_real > abs_imag) ? 
					(abs_real + abs_imag/2) : 
					(abs_imag + abs_real/2);		// Amplitude Approximation
		
		d_rssi = d_rssi - d_rssi/(1<<forgetting) + ampl_input; 	// Calculate Moving Average Filter = RSSI
		
		// RSSI delay produce
		d_array_delay[d_pointer] = d_rssi;			
		d_pointer ++;
		d_pointer %= d_detect_delay;				// Ringdelay
	//--------------------------------------------------------------------------------------
		if (d_array_delay[d_pointer] < ampl_input && 	// Signal detection?
			d_counter > d_Data_Samples)					// Could it be, that we are in the zero power symbol of the OFDM Frame?
		{
			out[0]=1;
			d_counter = 0;							// Reset samplecounter
		}
		else
		{
			out[0]=0;
			d_counter++;							// Count samples between two frames
		}
		
		if (d_counter >= 2000000)					// No framestart found?
		{
			printf ("No Signal :-( \n");
			d_counter = d_Data_Samples;				// Framestart-searching goes on
		}
		
		in++;
		input_used++;
		out++;
		output_generated_counter++;
	}
	
	consume_each(input_used);						// Used input values
	return output_generated_counter;				// Generated output values
}
