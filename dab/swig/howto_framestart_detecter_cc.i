GR_SWIG_BLOCK_MAGIC(howto,framestart_detecter_cc);

howto_framestart_detecter_cc_sptr howto_make_framestart_detecter_cc (unsigned int tu, 
                                                     unsigned int delta, 
                                                     unsigned int l);

class howto_framestart_detecter_cc : public gr_block
{
private:
  howto_framestart_detecter_cc (unsigned int tu, 
                        unsigned int delta, 
                        unsigned int l);
};
