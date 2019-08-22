# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.

reset_timestep 0

# Choose potential
pair_style	eam/alloy
pair_coeff 	* * CuNi.eam.alloy Ni Cu


# Setup neighbor style

neighbor	0.5 bin
neigh_modify delay 10 check yes

# Setup output: 
# Include are time averaged thermo-variables
# and in particular, each of the elements of the pressure tensor

variable energy equal etotal
variable energySq equal "etotal^2"

variable volume equal vol
variable volumeSq equal "vol^2"

variable my_press equal press
variable pressSq equal "press^2"

variable my_temp equal temp
variable tempSq equal "temp^2" 

variable pxx equal "c_thermo_press[1]"
variable pyy equal "c_thermo_press[2]"
variable pzz equal "c_thermo_press[3]"
variable pxy equal "c_thermo_press[4]"
variable pxz equal "c_thermo_press[5]"
variable pyz equal "c_thermo_press[6]"

variable pxx2 equal "c_thermo_press[1]^2"
variable pyy2 equal "c_thermo_press[2]^2"
variable pzz2 equal "c_thermo_press[3]^2"
variable pxy2 equal "c_thermo_press[4]^2"
variable pxz2 equal "c_thermo_press[5]^2"
variable pyz2 equal "c_thermo_press[6]^2"

# Computing Averages and Standard Deviations

fix aveEnergy all ave/time ${nevery} ${nrepeat} ${nfreq} v_energy mode scalar ave running
fix aveEnergySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_energySq mode scalar ave running
variable energySTD equal "sqrt(abs(f_aveEnergySq - f_aveEnergy^2))"
variable varAveEnergy equal f_aveEnergy

fix aveVolume all ave/time ${nevery} ${nrepeat} ${nfreq} v_volume mode scalar ave running
fix aveVolumeSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_volumeSq mode scalar ave running
variable volumeSTD equal "sqrt(abs(f_aveVolumeSq - f_aveVolume^2))"
variable varAveVolume equal f_aveVolume

fix avePress all ave/time ${nevery} ${nrepeat} ${nfreq} v_my_press mode scalar ave running
fix avePressSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pressSq mode scalar ave running
variable pressSTD equal "sqrt(abs(f_avePressSq - f_avePress^2))"
variable varAvePress equal f_avePress

fix aveTemp all ave/time ${nevery} ${nrepeat} ${nfreq} v_my_temp mode scalar ave running
fix aveTempSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_tempSq mode scalar ave running
variable tempSTD equal "sqrt(abs(f_aveTempSq - f_aveTemp^2))"
variable varAveTemp equal f_aveTemp

fix avePxx all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxx mode scalar ave running
fix avePyy all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyy mode scalar ave running
fix avePzz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pzz mode scalar ave running
fix avePxy all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxy mode scalar ave running
fix avePxz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxz mode scalar ave running
fix avePyz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyz mode scalar ave running
variable varAvePxx equal f_avePxx
variable varAvePyy equal f_avePyy
variable varAvePzz equal f_avePzz
variable varAvePxy equal f_avePxy
variable varAvePxz equal f_avePxz
variable varAvePyz equal f_avePyz

fix avePxxSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxx2 mode scalar ave running
fix avePyySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyy2 mode scalar ave running
fix avePzzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pzz2 mode scalar ave running
fix avePxySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxy2 mode scalar ave running
fix avePxzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxz2 mode scalar ave running
fix avePyzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyz2 mode scalar ave running

variable pxxSTD equal "sqrt(abs(f_avePxxSq - f_avePxx^2))"
variable pyySTD equal "sqrt(abs(f_avePyySq - f_avePyy^2))"
variable pzzSTD equal "sqrt(abs(f_avePzzSq - f_avePzz^2))"
variable pxySTD equal "sqrt(abs(f_avePxySq - f_avePxy^2))"
variable pxzSTD equal "sqrt(abs(f_avePxzSq - f_avePxz^2))"
variable pyzSTD equal "sqrt(abs(f_avePyzSq - f_avePyz^2))"






thermo		${nthermo}
thermo_style custom step temp v_varAveTemp v_tempSTD etotal v_varAveEnergy v_energySTD vol v_varAveVolume v_volumeSTD press v_varAvePress v_pressSTD pxx v_varAvePxx v_pxxSTD pxy v_varAvePxy v_pxySTD
thermo_modify norm no

# Setup MD

timestep ${TIMESTEP}
fix 4 all nve
fix 5 all langevin ${TEMPERATURE} ${TEMPERATURE} ${tdamp} ${RANDOM}


