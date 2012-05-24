/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
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
#include "config.h"
#endif

#include <stdio.h>

#include <howto_time_interleaving_vff.h>
#include <gr_io_signature.h>
 
 howto_time_interleaving_vff_sptr 
 howto_make_time_interleaving_vff(unsigned int ChSize)
{
  return howto_time_interleaving_vff_sptr (new howto_time_interleaving_vff (ChSize));
}

/*
 * The private constructor
 */

howto_time_interleaving_vff::howto_time_interleaving_vff (unsigned int ChSize)
  : gr_block ("time_interleaving_vff",
		   gr_make_io_signature (1, 1, sizeof (float)*ChSize*64/8),	// SubChannel Data (Vektor aufgesplittet in 8 Teile da GNU nicht sehr schlau)
		   gr_make_io_signature (1, 1, sizeof (float)*ChSize*64)),		
		   d_ChSize(ChSize),	// Subchannel Size
		   d_CIF_Fragment(0),	// Wievieltes Stueck des CIF Fragments (Acht Fragmente ergeben ein CIF)
		   d_DataArray()		// Datenarray mit Verzoegerten Daten
{
	unsigned int i;
	for(i=0;i<16*864*64;i++)	// Maximalgroesse des Arrays initialisieren 
	{
		d_DataArray[i]=0;
	}
}
//------------------------------------------------------------------------------------------
void
howto_time_interleaving_vff::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
		ninput_items_required[i] = 8;
}
//------------------------------------------------------------------------------------------
howto_time_interleaving_vff::~howto_time_interleaving_vff ()
{
}
//------------------------------------------------------------------------------------------
int 
howto_time_interleaving_vff::general_work (int noutput_items,
                               gr_vector_int &ninput_items,
                               gr_vector_const_void_star &input_items,
                               gr_vector_void_star &output_items)
{
	const float *in = (const float *) input_items[0];
	float *out = (float *) output_items[0];

	unsigned int input_samples = ninput_items[0];			// Nbr Inputsamples
	unsigned int input_used = 0;							// Index Inputvektor
	unsigned int input_used_counter = 0;					// Verbrauchte Inputvektoren zaehlen
	unsigned int output_generated_counter = 0;				// Anzahl generierte Outputvektoren
	unsigned int output_pointer = 0;						// Zeiger Outputvektor
	unsigned const int DelayArray [16] = {15,7,11,3,13,5,9,1,14,6,10,2,12,4,8,0};	// Wieviel die Bits (Mod 16) verzoegert werden sollen
	
//------------------------------------------------------------------------------------------
	unsigned int i;											// Schleifenvariable
//------------------------------------------------------------------------------------------

	while (input_used_counter < input_samples && output_generated_counter<noutput_items)
	{
	//------------------------------------------------------------------------------------------
		for (i=0;i<d_ChSize*64/8;i++)
		{
			d_DataArray[d_ChSize*64*DelayArray[i%16] + i + d_ChSize*64*d_CIF_Fragment/8] = in[input_used + i];				// Delay Array abfuellen
		}
		input_used+=d_ChSize*64/8;															// Inputarrays nachfahren
		input_used_counter++;
		
		if(d_CIF_Fragment==7)																// Ein CIF abgefuellt?
		{
			
			memcpy(&out[output_pointer], &d_DataArray[0], sizeof (float)*d_ChSize*64);		// Data SubChannel schreiben
			output_pointer += (d_ChSize*64);
			output_generated_counter ++;
			
			memcpy(&d_DataArray[0], &d_DataArray[d_ChSize*64], sizeof (float)*d_ChSize*64*15);	// DelayArray nachschieben
		}
		
		d_CIF_Fragment = (d_CIF_Fragment+1)%8;												// Acht Inputfragmente ergeben ein CIF
	}

	consume_each(input_used_counter);							// Wieviel vom Inputvektor gebruacht wurde
	return output_generated_counter;							// Anzahl Outputdaten
}
