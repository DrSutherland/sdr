GR_SWIG_BLOCK_MAGIC(howto,detect_cut_vcc);

howto_detect_cut_vcc_sptr howto_make_detect_cut_vcc (unsigned int tf,
                                                     unsigned int tu, 
                                                     unsigned int delta, 
                                                     unsigned int l);

class howto_detect_cut_vcc : public gr_block
{
private:
  howto_detect_cut_vcc (unsigned int tf, 
                        unsigned int tu, 
                        unsigned int delta, 
                        unsigned int l);
};
