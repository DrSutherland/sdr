/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
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
 
#ifndef INCLUDED_HOWTO_TIME_INTERLEAVING_VFF_H
#define INCLUDED_HOWTO_TIME_INTERLEAVING_VFF_H

#include <gr_block.h>

class howto_time_interleaving_vff;
 
  typedef boost::shared_ptr<howto_time_interleaving_vff> howto_time_interleaving_vff_sptr;
 
howto_time_interleaving_vff_sptr howto_make_time_interleaving_vff (unsigned int ChSize);

class howto_time_interleaving_vff : public gr_block
{
  private:
  friend howto_time_interleaving_vff_sptr howto_make_time_interleaving_vff (unsigned int ChSize);
  
  howto_time_interleaving_vff (unsigned int ChSize);  // private constructor
                         
  unsigned int d_ChSize;
  unsigned int d_CIF_Fragment;
  float d_DataArray[16*864*64];						// Array fuer maximale Subchannelgroesse initialisieren
                        
  public:
  ~howto_time_interleaving_vff ();
  
  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* HOWTO_TIME_INTERLEAVING_VFF_H */
