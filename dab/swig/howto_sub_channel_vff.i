GR_SWIG_BLOCK_MAGIC(howto,sub_channel_vff);

howto_sub_channel_vff_sptr howto_make_sub_channel_vff (unsigned int K, 
                                                       unsigned int StartArd, 
                                                       unsigned int ChSize);

class howto_sub_channel_vff : public gr_block
{
private:
  howto_sub_channel_vff (unsigned int K, 
                         unsigned int StartArd, 
                         unsigned int ChSize);
};
