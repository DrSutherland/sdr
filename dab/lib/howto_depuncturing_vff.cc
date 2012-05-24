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

#include <howto_depuncturing_vff.h>
#include <gr_io_signature.h>
 
 howto_depuncturing_vff_sptr 
 howto_make_depuncturing_vff(unsigned int ChSize,
							unsigned int PI1,
							unsigned int L1,
							unsigned int PI2,
							unsigned int L2,
							unsigned int PI3,
							unsigned int L3,
							unsigned int PI4,
							unsigned int L4)
{
  return howto_depuncturing_vff_sptr (new howto_depuncturing_vff (ChSize,PI1,L1,PI2,L2,PI3,L3,PI4,L4));
}

/*
 * The private constructor
 */

howto_depuncturing_vff::howto_depuncturing_vff (unsigned int ChSize,
												unsigned int PI1,
												unsigned int L1,
												unsigned int PI2,
												unsigned int L2,
												unsigned int PI3,
												unsigned int L3,
												unsigned int PI4,
												unsigned int L4)
  : gr_block ("depuncturing_vff",
		   gr_make_io_signature (1, 1, sizeof (float)*ChSize*64),
		   gr_make_io_signature (1, 1, sizeof (float)*((L1+L2+L3+L4)*32*4+24))),
		   d_ChSize(ChSize),			// Subchannel groesse
		   d_PI1(PI1),					// Puncturing Index Abschnitt 1
		   d_L1(L1),					// Laenge des Puncturing Index Abschnitts 1
		   d_PI2(PI2),					// Puncturing Index Abschnitt 2
		   d_L2(L2),					// Laenge des Puncturing Index Abschnitts 2
		   d_PI3(PI3),					// Puncturing Index Abschnitt 3
		   d_L3(L3),					// Laenge des Puncturing Index Abschnitts 3
		   d_PI4(PI4),					// Puncturing Index Abschnitt 4
		   d_L4(L4),					// Laenge des Puncturing Index Abschnitts 4
		   d_anz_punct_bits(),			// Vorbereitetes Array fuer abschnittlangenspeicherung
		   d_PI_array()					// Vorbereitetes Array fuer PI speicherung
{
	d_anz_punct_bits[0] = d_L1*32*4;	// Anzahl Bit Abschnitt 1 in Array abspeichern
	d_anz_punct_bits[1] = d_L2*32*4;	// Anzahl Bit Abschnitt 2 in Array abspeichern
	d_anz_punct_bits[2] = d_L3*32*4;	// Anzahl Bit Abschnitt 3 in Array abspeichern
	d_anz_punct_bits[3] = d_L4*32*4;	// Anzahl Bit Abschnitt 4 in Array abspeichern
	d_anz_punct_bits[4] = 24;			// Tail
	d_PI_array[0] = PI1;				// PI1 in Array abspeichern
	d_PI_array[1] = PI2;				// PI2 in Array abspeichern
	d_PI_array[2] = PI3;				// PI3 in Array abspeichern
	d_PI_array[3] = PI4;				// PI4 in Array abspeichern
	d_PI_array[4] = 8;					// Tail
}
//------------------------------------------------------------------------------------------
void
howto_depuncturing_vff::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
		ninput_items_required[i] = 1;
}
//------------------------------------------------------------------------------------------
howto_depuncturing_vff::~howto_depuncturing_vff ()
{
}
//------------------------------------------------------------------------------------------
int 
howto_depuncturing_vff::general_work (int noutput_items,
                               gr_vector_int &ninput_items,
                               gr_vector_const_void_star &input_items,
                               gr_vector_void_star &output_items)
{
	const float *in = (const float *) input_items[0];
	float *out = (float *) output_items[0];

	unsigned int input_samples = ninput_items[0];			// Nbr Inputsamples
	unsigned int input_used_counter = 0;					// Verbrauchte Inputvektoren zaehlen
	unsigned int output_generated_counter = 0;				// Anzahl generierte Outputvektoren
	
 unsigned const int PVs[24][32]= {{1,1,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0},	//PI1
	                              {1,1,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0},	//PI2
	                              {1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0},	//PI3
	                              {1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0},	//PI4
	                              {1,1,0,0, 1,1,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,0,0,0},	//PI5
	                              {1,1,0,0, 1,1,0,0, 1,1,0,0, 1,0,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,0,0,0},	//PI6
	                              {1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,0,0,0},	//PI7
	                              {1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0},	//PI8
	                              {1,1,1,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0},	//PI9
	                              {1,1,1,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,0,0, 1,1,0,0},	//PI10
	                              {1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,0,0, 1,1,0,0},	//PI11
	                              {1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0},	//PI12
	                              {1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,0,0},	//PI13
	                              {1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,0,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,0,0},	//PI14
	                              {1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,0,0},	//PI15
	                              {1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0},	//PI16
	                              {1,1,1,1, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0},	//PI17
	                              {1,1,1,1, 1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,0, 1,1,1,0},	//PI18
	                              {1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,0, 1,1,1,0},	//PI19
	                              {1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0},	//PI20
	                              {1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,0},	//PI21
	                              {1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0},	//PI22
	                              {1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0},	//PI23
	                              {1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1}};//PI24
	
//------------------------------------------------------------------------------------------
	unsigned int PV [32];						// Aktuell verwendeter Puncturing Vector
	unsigned int BlockNr;						// Wievielter Puncturing Block
	unsigned int Bit_counter;					// Bitcounter fuer die Datenbloecke
	unsigned int PV_zeiger=0;					// Zeiger innerhalb des PV
//------------------------------------------------------------------------------------------

	while (input_used_counter < input_samples && output_generated_counter<noutput_items)
	{
		for(BlockNr=0;BlockNr<5;BlockNr++)
		{
			memcpy(&PV[0], &PVs[d_PI_array[BlockNr]-1][0], sizeof (int)*32);		// Aktuell zu verwendender PV zuweisen
			
			for(Bit_counter=0;Bit_counter<d_anz_punct_bits[BlockNr];Bit_counter++)	// Bits eines Blocks durchlaufen
			{
				if (PV[PV_zeiger]==1)
				{
					out[0]=in[0];							// Bei einer "1" im PV wird ein Inputwert verwendet
					in++;
				}
				else
				{
					out[0]=0;								// Bei einer "0" im PV wird eine 0 verwendet
				}
				out++;										// Zeiger des Outputvektors anpassen
				
				PV_zeiger = (PV_zeiger+1)%32;
			}
		}
		input_used_counter++;
		output_generated_counter++;
	}
	
	consume_each(input_used_counter);							// Wieviel vom Inputvektor gebruacht wurde
	return output_generated_counter;							// Anzahl Outputdaten
}
