reset_timestep			0


thermo					500
thermo_style			custom step etotal pe temp vol press 
thermo_modify			norm no

dump 					1 all xyz 1000 dump.xyz
