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
 
#ifndef INCLUDED_HOWTO_SUB_CHANNEL_VFF_H
#define INCLUDED_HOWTO_SUB_CHANNEL_VFF_H

#include <gr_block.h>

class howto_sub_channel_vff;
 
  typedef boost::shared_ptr<howto_sub_channel_vff> howto_sub_channel_vff_sptr;
 
howto_sub_channel_vff_sptr howto_make_sub_channel_vff (unsigned int K, 
                                                       unsigned int StartArd, 
                                                       unsigned int ChSize);

class howto_sub_channel_vff : public gr_block
{
  private:
  friend howto_sub_channel_vff_sptr howto_make_sub_channel_vff (unsigned int K, 
                                                                unsigned int StartArd, 
                                                                unsigned int ChSize);
  
  howto_sub_channel_vff (unsigned int K, 
                         unsigned int StartArd, 
                         unsigned int ChSize);  // private constructor
                         
  enum state_t {STATE_Detect_First_Symbol, STATE_Handle_FIC, STATE_Handle_MSC};
  
  unsigned int d_tu;
  unsigned int d_K;
  unsigned int d_StartArd;
  unsigned int d_ChSize;
  state_t d_state;
  unsigned int d_SymbolNr;
  unsigned int d_Zeiger;
  unsigned int d_CU_counter;
  float d_FibMem[4*2304];
  float d_MSCMem[55296];
  float d_Dummy[9000];
                        
  public:
  ~howto_sub_channel_vff ();
  
  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* HOWTO_SUB_CHANNEL_VFF_H */
