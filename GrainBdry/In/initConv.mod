# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.

# Setup output

reset_timestep 0

variable energy equal etotal
variable energySq equal "etotal^2"

variable volume equal vol
variable volumeSq equal "vol^2"

variable my_press equal press
variable pressSq equal "press^2"

variable my_temp equal temp
variable tempSq equal "temp^2" 

variable my_enthalpy equal enthalpy
variable enthalpySq equal "enthalpy^2"


# Computing Averages and Standard Deviations

fix aveEnergy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_energy mode scalar ave window 20
fix aveEnergySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_energySq mode scalar ave window 20
variable energySTD equal "sqrt(abs(f_aveEnergySq - f_aveEnergy^2))"
variable varAveEnergy equal f_aveEnergy

fix aveVolume all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_volume mode scalar ave window 20
fix aveVolumeSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_volumeSq mode scalar ave window 20
variable volumeSTD equal "sqrt(abs(f_aveVolumeSq - f_aveVolume^2))"
variable varAveVolume equal f_aveVolume

fix avePress all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_press mode scalar ave window 20
fix avePressSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_pressSq mode scalar ave window 20
variable pressSTD equal "sqrt(abs(f_avePressSq - f_avePress^2))"
variable varAvePress equal f_avePress

fix aveTemp all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_temp mode scalar ave window 20
fix aveTempSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_tempSq mode scalar ave window 20
variable tempSTD equal "sqrt(abs(f_aveTempSq - f_aveTemp^2))"
variable varAveTemp equal f_aveTemp

fix aveEnthalpy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_enthalpy mode scalar ave window 20
fix aveEnthalpySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_enthalpySq mode scalar ave window 20
variable enthalpySTD equal "sqrt(abs(f_aveEnthalpySq - f_aveEnthalpy^2))"
variable varAveEnthalpy equal f_aveEnthalpy



thermo		${NFREQ}
thermo_style 	custom step temp v_varAveTemp v_tempSTD etotal v_varAveEnergy v_energySTD vol v_varAveVolume v_volumeSTD press v_varAvePress v_pressSTD enthalpy v_varAveEnthalpy v_enthalpySTD

# Setup MD

timestep 	${TIMESTEP}
fix 		1 all nve
fix 		2 all langevin ${TEMPERATURE} ${TEMPERATURE} $(v_TIMESTEP*100) ${RANDOM}


