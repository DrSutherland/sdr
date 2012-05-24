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
 
#ifndef INCLUDED_HOWTO_VITERBI_VFB_H
#define INCLUDED_HOWTO_VITERBI_VFB_H

#include <gr_block.h>

class howto_viterbi_vfb;
 
  typedef boost::shared_ptr<howto_viterbi_vfb> howto_viterbi_vfb_sptr;
 
howto_viterbi_vfb_sptr howto_make_viterbi_vfb (unsigned int Inputlaenge);

class howto_viterbi_vfb : public gr_block
{
  private:
  friend howto_viterbi_vfb_sptr howto_make_viterbi_vfb (unsigned int Inputlaenge);
  
  howto_viterbi_vfb (unsigned int Inputlaenge);  // private constructor
                         
  unsigned int d_Inputlaenge;
  unsigned int d_SpeicherTabs;
  unsigned int d_lange;
  unsigned int d_Pfad[64][2];
  float d_Ref[128][4];				// Array welcher das Optimale-Empfangsergebnis enthält
                        
  public:
  ~howto_viterbi_vfb ();
  
  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* HOWTO_VITERBI_VFB_H */
