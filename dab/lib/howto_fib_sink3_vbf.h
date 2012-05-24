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
 
#ifndef INCLUDED_HOWTO_fib_sink3_vbf_H
#define INCLUDED_HOWTO_fib_sink3_vbf_H

#include <gr_block.h>

class howto_fib_sink3_vbf;
 
  typedef boost::shared_ptr<howto_fib_sink3_vbf> howto_fib_sink3_vbf_sptr;
 
howto_fib_sink3_vbf_sptr howto_make_fib_sink3_vbf ();

class howto_fib_sink3_vbf : public gr_block
{
  private:
  friend howto_fib_sink3_vbf_sptr howto_make_fib_sink3_vbf ();
  int BinToDez(const char *FIG, int startPos, int laenge);
  void Type1Extension1(const char *FIG, int Offset, int AnzByte);
  void Type0Extension2(const char *FIG, int Offset, int BitLength);
  void Type0Extension1(const char *FIG, int Offset, int BitLength);
  void Type0Extension10(const char *FIG, int Offset);
  void Type0Extension9(const char *FIG, int Offset);
  
  howto_fib_sink3_vbf ();  // private constructor
  
  char d_serviceLabel [64][16];
  int d_datenbank [64][8];
  int d_dateTime [8];			// Jahr/Monat/Tag/Stunde/Minute/Second/OffsetStunde/OffsetMinute
  
  
  public:
  ~howto_fib_sink3_vbf ();
  
  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* HOWTO_fib_sink3_vbf_H */
