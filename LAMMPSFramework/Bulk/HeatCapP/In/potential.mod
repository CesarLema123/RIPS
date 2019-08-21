# Specify the potential and neighbor range.

pair_style 		eam/alloy
pair_coeff 		* * CuNi.eam.alloy Ni Cu  
neighbor 		.05 bin
neigh_modify 	delay 10 check yes

