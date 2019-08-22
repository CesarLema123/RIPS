
# Reset the timestep, make any changes to how the simulation is run, and change what and how often things are output


reset_timestep			0

# Remove the drag factor from the actual run (it was used during convergence)
fix						1 all nph iso ${PRESSURE} ${PRESSURE} $(dt*v_kP)
fix 					2 all langevin ${TEMPERATURE} ${TEMPERATURE} $(dt*v_kT) ${RANDOM} zero yes

# Compute the mean square displacement of atoms for diffusion coeff.
compute 				MSD all msd com yes

# specify how often things are output to the log
thermo					200
thermo_style			custom step temp press c_MSD[4]
thermo_modify			norm no

# dump the position data for visualization
dump 					1 all xyz 1000 dump.xyz
