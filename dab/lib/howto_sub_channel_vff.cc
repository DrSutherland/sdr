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

#include <howto_sub_channel_vff.h>
#include <gr_io_signature.h>
 
 howto_sub_channel_vff_sptr 
 howto_make_sub_channel_vff(unsigned int K, 
                            unsigned int StartArd, 
                            unsigned int ChSize)
{
  return howto_sub_channel_vff_sptr (new howto_sub_channel_vff (K,StartArd,ChSize));
}

/*
 * The private constructor
 */

howto_sub_channel_vff::howto_sub_channel_vff (unsigned int K, 
                                              unsigned int StartArd,
                                              unsigned int ChSize)
  : gr_block ("sub_channel_vff",
		   gr_make_io_signature2 (2, 2, sizeof (float)*K*2, sizeof (char)),
		   gr_make_io_signature2 (1, 2, sizeof (float)*ChSize*64/8, sizeof (float)*2304/8)),		// SubChannel Data und FIB (Vektor aufgesplittet in 8 Teile da GNU nicht sehr schlau)
		   d_K(K),
		   d_StartArd(StartArd),
		   d_ChSize(ChSize),
		   d_state(STATE_Detect_First_Symbol),
		   d_SymbolNr(0),
		   d_Zeiger(0),
		   d_CU_counter(0),
		   d_FibMem(),
		   d_MSCMem()
{
	set_relative_rate((4*8)/76);
}
//------------------------------------------------------------------------------------------
void
howto_sub_channel_vff::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
		ninput_items_required[i] = (double) 76/(double)(4*8);		// Mode 1 -> 76 Symbole = 4 CIF in einem Frame
}
//------------------------------------------------------------------------------------------
howto_sub_channel_vff::~howto_sub_channel_vff ()
{
}
//------------------------------------------------------------------------------------------
int 
howto_sub_channel_vff::general_work (int noutput_items,
                               gr_vector_int &ninput_items,
                               gr_vector_const_void_star &input_items,
                               gr_vector_void_star &output_items)
{
	const float *in = (const float *) input_items[0];
	char const *in2 = (const char *) input_items[1];
	float *out = (float *) output_items[0];
	float *out2 = (float *) output_items[1];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples
	unsigned int input_samples2 = ninput_items[1];	// Nbr Inputsamples
	unsigned int input_used = 0;					// Index Inputvektor
	unsigned int input_used2 = 0;					// Index Inputvektor
	unsigned int output_generated = 0;				// Index Outputvektor
	unsigned int output_pointer = 0;
	unsigned int output_pointer2 = 0;
	
//------------------------------------------------------------------------------------------
	unsigned int i;									// Zaehlvariabel fuer FOR Schleife
	unsigned int FIB_Nr;							// FIB Nummer im Frame (Zwischenspeicher)
//------------------------------------------------------------------------------------------

	while (input_used2 < input_samples && input_used2 < input_samples2 && output_generated+8<noutput_items)
	{
	//------------------------------------------------------------------------------------------
		switch (d_state)
		{
			case(STATE_Detect_First_Symbol):
				if (in2[input_used2] == 1)
				{
					d_SymbolNr = 0;
					d_state = STATE_Handle_FIC;						// Wegen differentieller Modulation erstes Symbol unbrauchbar
				}
				break;
			//------------------------------------------------------------------------------------------
			case(STATE_Handle_FIC):
				if (d_SymbolNr == 1)
				{
					memcpy(&d_FibMem[0], &in[input_used], sizeof (float)*3072);				// FIC 1 speichern
				}
				if (d_SymbolNr == 2) 
				{
					memcpy(&d_FibMem[3072], &in[input_used], sizeof (float)*3072);			// FIC 2 speichern
				}
				if (d_SymbolNr == 3) 
				{
						memcpy(&d_FibMem[6144], &in[input_used], sizeof (float)*3072);		// FIC 3 speichern
						d_state = STATE_Handle_MSC;
				}
				break;
			//------------------------------------------------------------------------------------------
			case(STATE_Handle_MSC):
				if (d_SymbolNr == 4 || d_SymbolNr == 22 || d_SymbolNr == 40 || d_SymbolNr == 58)	// Für DAB Mode 1
				{
					d_Zeiger = 0;
					d_CU_counter = 0;
				}
				
				for (i = 0;i<48;i++)																// CUs eines Samples durchlaufen
				{
					if (d_CU_counter >= d_StartArd && d_CU_counter < (d_StartArd+d_ChSize))
					{
						memcpy(&d_MSCMem[d_Zeiger*64], &in[input_used+i*64], sizeof (float)*64);	// Gewünschter Subchannel abspeichern
						d_Zeiger++;
					}
					
					if (d_CU_counter == (d_StartArd+d_ChSize-1))										// MSC Komplett
					{
						FIB_Nr = (d_SymbolNr-4)/18;
						memcpy(&out2[output_pointer2], &d_FibMem[FIB_Nr*2304], sizeof (float)*2304);	// FIB Block schreiben
						output_pointer2 += 2304;
						
						memcpy(&out[output_pointer], &d_MSCMem[0], sizeof (float)*d_ChSize*64);		// Data SubChannel schreiben
						output_pointer += (d_ChSize*64);
						
						output_generated += 8;
					}
					
					d_CU_counter++;
				}
				break;
		}
		//------------------------------------------------------------------------------------------
		d_SymbolNr++;
		if (d_SymbolNr >= 76)							// Frame Ende oder es ist ein Ueberlauf aufgetreten (Statemachine-Neustart)
		{
			d_state = STATE_Detect_First_Symbol;
		}
		
		input_used+=3072;								// Inputarrays nachfahren
		input_used2++;
	}

	consume_each(input_used2);							// Wieviel vom Inputvektor gebruacht wurde
	return output_generated;							// Anzahl Outputdaten
}
