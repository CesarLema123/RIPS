# Specify the initial inputs for the simulation

# variable 		TIMESTEP equal 0.0001 Should be specified in the header of in.*


clear
units 			metal
dimension 		3
boundary 		p p p
atom_style 		atomic

timestep		${TIMESTEP}
