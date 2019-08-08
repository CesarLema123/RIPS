# Specify the initial inputs for the simulation

clear
units 			metal
dimension 		3
boundary 		p p p
atom_style 		atomic
read_data		${DATAFILE}
