GR_SWIG_BLOCK_MAGIC(howto,depuncturing_vff);

howto_depuncturing_vff_sptr howto_make_depuncturing_vff (unsigned int ChSize,
												unsigned int PI1,
												unsigned int L1,
												unsigned int PI2,
												unsigned int L2,
												unsigned int PI3,
												unsigned int L3,
												unsigned int PI4,
												unsigned int L4);

class howto_depuncturing_vff : public gr_block
{
private:
  howto_depuncturing_vff (unsigned int ChSize,
												unsigned int PI1,
												unsigned int L1,
												unsigned int PI2,
												unsigned int L2,
												unsigned int PI3,
												unsigned int L3,
												unsigned int PI4,
												unsigned int L4);
};
