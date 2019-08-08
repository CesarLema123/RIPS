# Specify the potential and neighbor range.

pair_style 		eam/alloy
pair_coeff 		* * CuNi.eam.alloy Ni Cu  
neighbor 		.05 bin
neigh_modify 		delay 10 check yes



timestep		${TIMESTEP}
reset_timestep		0

# -------------------- SET UP COMPUTES AND FIX AVE/TIME -------------------- 
# AVERAGE AND STANDARD DEVIATION 
# TEMPERATURE 
variable 		TEMP equal temp
fix			aveTemp all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_TEMP mode scalar ave running
variable		varAveTemp equal "f_aveTemp"
variable		tempSq equal "v_TEMP^2"
fix			aveTempSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_tempSq mode scalar ave running
variable		tempSTD equal "sqrt(f_aveTempSq - f_aveTemp^2)"

# PRESSURE
variable		PRESS equal press
fix 			avePress all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_PRESS mode scalar ave running
variable		varAvePress equal "f_avePress"
variable		pressSq equal "v_PRESS^2"
fix 			avePressSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_pressSq mode scalar ave running
variable 		pressSTD equal "sqrt(f_avePressSq - f_avePress^2)"

# ENERGY
variable		ENERGY equal etotal
fix			aveEnergy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_ENERGY mode scalar ave running
variable 		varAveEnergy equal "f_aveEnergy"
variable		energySq equal "v_ENERGY^2"
fix			aveEnergySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_energySq mode scalar ave running
variable		energySTD equal "sqrt(f_aveEnergySq - f_aveEnergy^2)"

# VOLUME
variable		VOLUME equal vol
fix			aveVolume all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_VOLUME mode scalar ave running
variable 		varAveVolume equal "f_aveVolume"
variable		volumeSq equal "v_VOLUME^2"
fix			aveVolumeSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_volumeSq mode scalar ave running 
variable		volumeSTD equal "sqrt(abs(f_aveVolumeSq - f_aveVolume^2))"

# ENTHALPY
variable                ENTH equal enthalpy
fix                     aveEnthalpy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_ENTH mode scalar ave running
variable                varAveEnthalpy equal "f_aveEnthalpy"
variable                enthalpySq equal "v_ENTH^2"
fix                     aveEnthalpySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_enthalpySq mode scalar ave running
variable                enthalpySTD equal "sqrt(f_aveEnthalpySq - f_aveEnthalpy^2)"

thermo			${NTHERMO}
thermo_style		custom step etotal v_varAveEnergy v_energySTD enthalpy v_varAveEnthalpy v_enthalpySTD temp v_varAveTemp v_tempSTD vol v_varAveVolume v_volumeSTD press v_varAvePress v_pressSTD


fix			1 all nph iso ${PRESSURE} ${PRESSURE} ${dampP} 
fix			2 all langevin ${TEMPERATURE} ${TEMPERATURE} ${dampT} ${RANDOM} zero yes 


