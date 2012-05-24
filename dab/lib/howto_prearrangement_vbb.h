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
 
#ifndef INCLUDED_HOWTO_prearrangement_VBB_H
#define INCLUDED_HOWTO_prearrangement_VBB_H

#include <gr_block.h>

class howto_prearrangement_vbb;
 
  typedef boost::shared_ptr<howto_prearrangement_vbb> howto_prearrangement_vbb_sptr;
 
howto_prearrangement_vbb_sptr howto_make_prearrangement_vbb (unsigned int InVectorSize);

class howto_prearrangement_vbb : public gr_block
{
  private:
  friend howto_prearrangement_vbb_sptr howto_make_prearrangement_vbb (unsigned int InVectorSize);
  
  howto_prearrangement_vbb (unsigned int InVectorSize);  // private constructor
                         
  unsigned int d_timeinterleaverBridge;
  unsigned int d_InVectorSize;
                        
  public:
  ~howto_prearrangement_vbb ();
  
  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* HOWTO_prearrangement_VBB_H */
