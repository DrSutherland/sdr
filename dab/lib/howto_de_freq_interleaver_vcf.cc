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

#include <howto_de_freq_interleaver_vcf.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of de_freq_interleaver_vcf and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_de_freq_interleaver_vcf_sptr 
 howto_make_de_freq_interleaver_vcf(unsigned int tu, unsigned int K)
{
  return howto_de_freq_interleaver_vcf_sptr (new howto_de_freq_interleaver_vcf (tu,K));
}

/*
 * The private constructor
 */

howto_de_freq_interleaver_vcf::howto_de_freq_interleaver_vcf (unsigned int tu, unsigned int K)
  : gr_block ("de_freq_interleaver_vcf",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)*tu),
		   gr_make_io_signature (1, 1, sizeof (float)*K*2)),
		   d_tu(tu), 				// FFT laenge (Standard EN 300 401 Page 145)
		   d_K(K),					// Anzahl Subcarrier (Standard EN 300 401 Page 145)
		   d_deinterleaver()
{
    int work [d_tu][5];
    int counter = 0;
    
    int i;
    for (i=0;i<d_tu;i++)
    {
         work[i][0] = i;                                     // Spalte 1 erzeugen ETSI EN 300 401 Seite 158
    }
    
    work [0][1] = 0;
    for (i=1;i<d_tu;i++)
    {
		work [i][1] = (13*work[i-1][1]+(d_tu/4-1)) % d_tu;  // Spalte 2 erzeugen ETSI EN 300 401 Seite 158
		
		if (!((work [i][1] < ((d_tu/8))) ||
		    (work [i][1] > ((d_tu*7/8))) ||
		    (i == (d_tu/2))))
		{
			work [i][2] = work [i][1];                      // Spalte 3 erzeugen ETSI EN 300 401 Seite 158
			
			d_deinterleaver [counter] = work [i][2];          // Zeigt wo sich das Bit für den Zielvektor im FFT Vektor befindet
			counter++;
		}
	}
}
//------------------------------------------------------------------------------------------
void
howto_de_freq_interleaver_vcf::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = 1;		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
}
//------------------------------------------------------------------------------------------
howto_de_freq_interleaver_vcf::~howto_de_freq_interleaver_vcf ()
{
}
//------------------------------------------------------------------------------------------
int 
howto_de_freq_interleaver_vcf::general_work (int noutput_items,
                               gr_vector_int &ninput_items,
                               gr_vector_const_void_star &input_items,
                               gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];
	float *out = (float *) output_items[0];

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples
	unsigned int input_used = 0;					// Index Inputvektor
	unsigned int output_generated = 0;				// Index Outputvektor

	for (int i = 0; (i < input_samples && output_generated < noutput_items); i++)
	{
		for (unsigned int j = 0; j < d_K; j++)
		{
			out[j] = in[d_deinterleaver[j]].real();		// Frequency Deinterleaving und Symbol Demapping
			out[j+d_K] = in[d_deinterleaver[j]].imag();
		}
		out += d_K*2;									// Zeiger aktuallisieren
		in  += d_tu;
		output_generated++;
		input_used ++;
	}

	consume_each(input_used);							// Wieviel vom Inputvektor gebruacht wurde
	return output_generated;							// Anzahl Outputdaten
}
