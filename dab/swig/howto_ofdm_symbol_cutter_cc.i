GR_SWIG_BLOCK_MAGIC(howto,ofdm_symbol_cutter_cc);

howto_ofdm_symbol_cutter_cc_sptr howto_make_ofdm_symbol_cutter_cc (unsigned int tf,
                                                     unsigned int tu, 
                                                     unsigned int delta, 
                                                     unsigned int l,
                                                     unsigned int offset);

class howto_ofdm_symbol_cutter_cc : public gr_block
{
private:
  howto_ofdm_symbol_cutter_cc (unsigned int tf,
                        unsigned int tu, 
                        unsigned int delta, 
                        unsigned int l,
                        unsigned int offset);
};
