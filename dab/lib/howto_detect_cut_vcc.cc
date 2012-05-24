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

#include <howto_detect_cut_vcc.h>
#include <gr_io_signature.h>

/*
 * Create a new instance of etect_cut_vcc and return
 * a boost shared_ptr.  This is effectively the public constructor.
 */
 
 howto_detect_cut_vcc_sptr 
 howto_make_detect_cut_vcc(unsigned int tf,	
                           unsigned int tu,
                           unsigned int delta,
                           unsigned int l)
{
  return howto_detect_cut_vcc_sptr (new howto_detect_cut_vcc (tf, tu, delta, l));
}

/*
 * The private constructor
 */
howto_detect_cut_vcc::howto_detect_cut_vcc (unsigned int tf,
                                            unsigned int tu,
                                            unsigned int delta,
                                            unsigned int l)
  : gr_block ("detect_cut_vcc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)),
		   gr_make_io_signature2 (2, 2, sizeof (gr_complex)*tu, sizeof (char))),
		   d_tf(tf), 				// Gesamt Framelange (Standard EN 300 401 Page 145)
		   d_tu(tu), 				// FFT laenge (Standard EN 300 401 Page 145)
		   d_delta(delta), 			// GardTime (Standard EN 300 401 Page 145)
		   d_l(l), 					// Anzahl Symbole (Standard EN 300 401 Page 145)
		   d_state(STATE_Detect), 	// Start State
		   d_counter(0), 			// Zaehlvariable
		   d_symbol(0), 			// Aktuelles Symbol
		   d_rssi(1000),			// RSSI Startwert
		   d_pointer(0),			// Zeiger fuer Delay
		   d_detect_delay(128),		// RSSI Delay groesse
		   d_array_delay(),			// RSSI Delay Array
		   d_offset(150)			// Nach Detection bis zur ersten FFT-Block-Bildung
{
  set_relative_rate((double)(l)/(double)tf);
  
  int n;
  for (n=0; n<d_detect_delay; n++)
  {
	  d_array_delay [n] = 1000;
  }
}

void
howto_detect_cut_vcc::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	unsigned ninputs = ninput_items_required.size ();
	for (unsigned i = 0; i < ninputs; i++)
		ninput_items_required[i] = d_tf/d_l;		// Grobe Schaetzung wieviele Inputsamples fuer einen Ausgangswert benoetigt werden
}

/*
 * Our virtual destructor.
 */
howto_detect_cut_vcc::~howto_detect_cut_vcc ()
{
  // nothing else required in this example
}

int
howto_detect_cut_vcc::general_work (int noutput_items,
			                        gr_vector_int &ninput_items,
			                        gr_vector_const_void_star &input_items,
			                        gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex *) input_items[0];		// (Input) Datenvektor
  
	gr_complex *optr = (gr_complex *) output_items[0];				// Outputdata
	char *out = (char *) output_items[1];							// '1' = First DAB Symbol

	unsigned int input_samples = ninput_items[0];	// Nbr Inputsamples
	unsigned int input_index = 0;					// Index Inputvektor
	unsigned int output_index = 0;					// Index Outputvektor
	
//------------------------------------------------------------------------------------------

	bool enough_sample_to_work = true;						// true = nach Statewechsel genug samples zum weiterverarbeiten 
	double ampl_input;										// Absolutwert eines komplexen Inputsamples
	double abs_real;										// Betrag des Realanteils
	double abs_imag;										// Betrag des Imaginaeranteils
	const unsigned int forgetting = 3;						// Vergessensfaktor
	unsigned int Data_Samples;								// Samples im FIC und MSC
	
	while (enough_sample_to_work == true)
	{
		switch (d_state) {
			//------------------------------------------------------------------------------------------
			case(STATE_Detect):									// Start eines DAB Frames detektieren
				d_symbol = 0;
				Data_Samples = d_l*(d_delta+d_tu);				// Samples im FIC und MSC
				
				while (input_index < input_samples)
				{
					abs_real = (in[input_index].real() > 0) ? 
							   (in[input_index].real()) : 
							   (-in[input_index].real());		// ABS des Realwert bilden
							   
					abs_imag = (in[input_index].imag() > 0) ? 
							   (in[input_index].imag()) : 
							   (-in[input_index].imag());		// ABS des Imagwert bilden
					
					ampl_input = (abs_real > abs_imag) ? 
								(abs_real + abs_imag/2) : 
								(abs_imag + abs_real/2);		// Amplituden Approximation
								
					
					d_rssi = d_rssi - d_rssi/(1<<forgetting) + ampl_input; 	// RSSI über Moving Average Filter berechnen
					
					d_array_delay[d_pointer] = d_rssi;			// RSSI delay (fuer detektion)
					d_pointer ++;
					d_pointer %= d_detect_delay;				// Ringdelay

					if (d_array_delay[d_pointer] < ampl_input && 	// Detektion ueberpruefen
						d_counter > Data_Samples)					// Befindet man sich wieder im Nullsymbol
					{
						d_state = STATE_Offset;
						printf ("Frame Distance: %6d  DifOptimal: %3d  ABS %+9f  RSSI %+9f \n", 
															   d_counter,
															   196608 - d_counter,
															   ampl_input,
															   d_array_delay[d_pointer]);
						d_counter = 0;							// Samplezaehler zuruecksetzen
						break;									// Aus while Detektions while Schleife springen
					}
					else
						d_counter++;							// Samples zwischen zwei DAB Frames zaehlen
					
					if (d_counter >= 2000000)					// Kein Framestart gefunden
					{
						printf ("No Signal: Real %+9f  Imag %+9f  ABS %+9f  RSSI %+9f \n",
															   in[input_index].real(),
															   in[input_index].imag(),
															   ampl_input,
															   d_array_delay[d_pointer]);
						d_counter = 0;						   // Samplezaehler zuruecksetzen
					}
					
					input_index++;
				}
				enough_sample_to_work = false;					// Keine Samples mehr vorhanden zum weiterarbeiten
				break;
				
			//------------------------------------------------------------------------------------------
			
			case(STATE_Offset):
				if ((input_index + d_offset) < input_samples)
				{
					input_index += d_offset;					// Offset einrechnen, damit FFT in der Mitte eines Symbols gemacht wird
					d_counter += d_offset;
					d_state = STATE_Symbol;
				}
				else
					enough_sample_to_work = false;				// Keine Samples mehr vorhanden zum weiterarbeiten
				break;
				
			//------------------------------------------------------------------------------------------
				
			case(STATE_Symbol):
				if ((input_index + d_tu) < input_samples)
				{
					memcpy(&optr[output_index], &in[input_index], d_tu*sizeof(gr_complex));		// Samples fuer FFT als Block herausgeben
					out[output_index] = (d_symbol==0) ? 1:0;									// Erstes Symbol in DAB Frame markieren
					output_index++;
					input_index += d_tu;
					d_counter += d_tu;
					
					d_symbol ++;
					d_state = (d_symbol >= d_l)? STATE_Detect : STATE_GuardTime;		// Ende des Frames erreicht?
				}
				else
					enough_sample_to_work = false;				// Keine Samples mehr vorhanden zum weiterarbeiten
				break;
				
			//------------------------------------------------------------------------------------------
				
			case(STATE_GuardTime):
				if ((input_index + d_delta) < input_samples)
				{
					input_index += d_delta;						// GuardTime einrechnen, damit FFT in der Mitte des naechsten Symbols gemacht wird
					d_counter += d_delta;	
					d_state = STATE_Symbol;
				}
				else 
					enough_sample_to_work = false;				// Keine Samples mehr vorhanden zum weiterarbeiten
				break;
			
			//------------------------------------------------------------------------------------------
		}
	}
	consume_each(input_index);						// Wieviel vom Inputvektor gebruacht wurde
	return output_index;							// Anzahl Outputdaten
}
