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
 
#ifndef INCLUDED_HOWTO_FIB_SINK_VB_H
#define INCLUDED_HOWTO_FIB_SINK_VB_H

#include <gr_sync_block.h>

class howto_fib_sink_vb;
 
  typedef boost::shared_ptr<howto_fib_sink_vb> howto_fib_sink_vb_sptr;
 
howto_fib_sink_vb_sptr howto_make_fib_sink_vb ();

class howto_fib_sink_vb : public gr_sync_block
{
  private:
  friend howto_fib_sink_vb_sptr howto_make_fib_sink_vb ();
  int BinToDez(const char *FIG, int startPos, int laenge);
  void DisplayLabel(const char *FIG, int Offset, int AnzByte);
  
  howto_fib_sink_vb ();  // private constructor
                         
                        
  public:
  ~howto_fib_sink_vb ();
  
  int work (int noutput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items);
};


#endif /* HOWTO_FIB_SINK_VB_H */
