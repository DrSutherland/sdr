GR_SWIG_BLOCK_MAGIC(howto,bonder_vff);

howto_bonder_vff_sptr howto_make_bonder_vff (unsigned int VectorInSize, unsigned int VectorOutSize);

class howto_bonder_vff : public gr_block
{
private:
  howto_bonder_vff (unsigned int VectorInSize, unsigned int VectorOutSize);
};
