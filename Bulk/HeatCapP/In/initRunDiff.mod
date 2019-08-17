reset_timestep			0

fix						1 all nph iso ${PRESSURE} ${PRESSURE} $(dt*v_kP)
fix 					2 all langevin ${TEMPERATURE} ${TEMPERATURE} $(dt*v_kT) ${RANDOM} zero yes


thermo					200
thermo_style			custom step enthalpy temp press
thermo_modify			norm no

