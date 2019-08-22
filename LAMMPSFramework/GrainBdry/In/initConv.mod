
# Specify averaging variables - 
# NEVERY: Use 1 out of every NEVERY value in averaging
# NREPEAT: NREPEAT observation in computing the average
# NFREQ: Output the average every NFREQ timesteps (must be an integer multiple of NEVER*NREPEAT)

variable NEVERY equal 10
variable NREPEAT equal 100
variable NFREQ equal $(v_NEVERY*v_NREPEAT)


reset_timestep 0


# Making variables of the thermodynamic values to be time-averaged.
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


# Computing Averages and Standard Deviations of the thermodynamic variables listed above

fix aveEnergy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_energy mode scalar ave running
fix aveEnergySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_energySq mode scalar ave running
variable energySTD equal "sqrt(abs(f_aveEnergySq - f_aveEnergy^2))"
variable varAveEnergy equal f_aveEnergy

fix aveVolume all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_volume mode scalar ave running
fix aveVolumeSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_volumeSq mode scalar ave running
variable volumeSTD equal "sqrt(abs(f_aveVolumeSq - f_aveVolume^2))"
variable varAveVolume equal f_aveVolume

fix avePress all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_press mode scalar ave running
fix avePressSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_pressSq mode scalar ave running
variable pressSTD equal "sqrt(abs(f_avePressSq - f_avePress^2))"
variable varAvePress equal f_avePress

fix aveTemp all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_temp mode scalar ave running
fix aveTempSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_tempSq mode scalar ave running
variable tempSTD equal "sqrt(abs(f_aveTempSq - f_aveTemp^2))"
variable varAveTemp equal f_aveTemp

fix aveEnthalpy all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_enthalpy mode scalar ave running
fix aveEnthalpySq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_enthalpySq mode scalar ave running
variable enthalpySTD equal "sqrt(abs(f_aveEnthalpySq - f_aveEnthalpy^2))"
variable varAveEnthalpy equal f_aveEnthalpy


# Set up the log output to display all of the values above.

thermo		${NFREQ}
thermo_style 	custom step temp v_varAveTemp v_tempSTD etotal v_varAveEnergy v_energySTD vol v_varAveVolume v_volumeSTD press v_varAvePress v_pressSTD enthalpy v_varAveEnthalpy v_enthalpySTD
thermo_modify 	norm no

