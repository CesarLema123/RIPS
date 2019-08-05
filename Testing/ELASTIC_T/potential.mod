# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.

reset_timestep 0

# Choose potential
pair_style	eam/alloy
pair_coeff 	* * CuNi.eam.alloy Ni Cu


# Setup neighbor style

neighbor	0.5 bin
neigh_modify delay 10 check yes

# Setup output
variable energy equal etotal
variable energySq equal "etotal^2"
variable volume equal vol
variable volumeSq equal "vol^2"
variable my_press equal press
variable pressSq equal pressSq
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

fix aveEnergy all ave/time ${nevery} ${nrepeat} ${nfreq} v_energy mode scalar
fix aveEnergySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_energySq mode scalar
fix aveVolue all ave/time ${nevery} ${nrepeat} ${nfreq} v_volume mode scalar
fix aveVolueSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_volumeSq mode scalar
fix avePress all ave/time ${nevery} ${nrepeat} ${nfreq} v_my_press mode scalar
fix avePressSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pressSq mode scalar
fix aveTemp all ave/time ${nevery} ${nrepeat} ${nfreq} v_my_temp mode scalar
fix aveTempSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_tempSq mode scalar
fix avePxx all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxx mode scalar
fix avePyy all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyy mode scalar
fix avePzz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pzz mode scalar
fix avePxy all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxy mode scalar
fix avePxz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxz mode scalar
fix avePyz all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyz mode scalar
fix avePxxSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxx2 mode scalar
fix avePyySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyy2 mode scalar
fix avePzzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pzz2 mode scalar
fix avePxySq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxy2 mode scalar
fix avePxzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pxz2 mode scalar
fix avePyzSq all ave/time ${nevery} ${nrepeat} ${nfreq} v_pyz2 mode scalar

thermo		${nthermo}
thermo_style custom step temp f_avt etotal f_avE vol f_avv press f_avp[1] f_avp[2] f_avp[3] f_avp[4] f_avp[5] f_avp[6] 
thermo_modify norm no

# Setup MD

timestep ${TIMESTEP}
fix 4 all nve
fix 5 all langevin ${TEMPERATURE} ${TEMPERATURE} ${tdamp} ${RANDOM}


