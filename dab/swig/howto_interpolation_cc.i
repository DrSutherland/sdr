GR_SWIG_BLOCK_MAGIC(howto,interpolation_cc);

howto_interpolation_cc_sptr howto_make_interpolation_cc (unsigned int interpolation,
                           unsigned int decimation);

class howto_interpolation_cc : public gr_block
{
private:
  howto_interpolation_cc (unsigned int interpolation,
                           unsigned int decimation);
};
