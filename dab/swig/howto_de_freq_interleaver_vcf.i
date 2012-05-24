GR_SWIG_BLOCK_MAGIC(howto,de_freq_interleaver_vcf);

howto_de_freq_interleaver_vcf_sptr howto_make_de_freq_interleaver_vcf (unsigned int tu, unsigned int K);

class howto_de_freq_interleaver_vcf : public gr_block
{
private:
  howto_de_freq_interleaver_vcf (unsigned int tu, unsigned int K);
};
