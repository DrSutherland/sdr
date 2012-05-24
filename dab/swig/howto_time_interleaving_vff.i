GR_SWIG_BLOCK_MAGIC(howto,time_interleaving_vff);

howto_time_interleaving_vff_sptr howto_make_time_interleaving_vff (unsigned int ChSize);

class howto_time_interleaving_vff : public gr_block
{
private:
  howto_time_interleaving_vff (unsigned int ChSize);
};
