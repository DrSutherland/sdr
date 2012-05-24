GR_SWIG_BLOCK_MAGIC(howto,cutter_vbb);

howto_cutter_vbb_sptr howto_make_cutter_vbb (unsigned int VectorInSize, unsigned int VectorOutSize);

class howto_cutter_vbb : public gr_block
{
private:
  howto_cutter_vbb (unsigned int VectorInSize, unsigned int VectorOutSize);
};
