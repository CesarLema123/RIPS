reset_timestep			0




thermo					1000
thermo_style			custom step vol press
thermo_modify			norm no

dump 					1 all xyz 1000 dump.xyz
