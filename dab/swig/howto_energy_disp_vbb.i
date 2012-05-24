GR_SWIG_BLOCK_MAGIC(howto,energy_disp_vbb);

howto_energy_disp_vbb_sptr howto_make_energy_disp_vbb (unsigned int ChSize);

class howto_energy_disp_vbb : public gr_block
{
private:
  howto_energy_disp_vbb (unsigned int ChSize);
};
