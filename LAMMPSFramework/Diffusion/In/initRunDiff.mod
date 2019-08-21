reset_timestep			0

fix						1 all nph iso ${PRESSURE} ${PRESSURE} $(dt*v_kP)
fix 					2 all langevin ${TEMPERATURE} ${TEMPERATURE} $(dt*v_kT) ${RANDOM} zero yes

compute 				MSD all msd com yes

thermo					200
thermo_style			custom step temp press c_MSD[4]
thermo_modify			norm no

dump 					1 all xyz 1000 dump.xyz
