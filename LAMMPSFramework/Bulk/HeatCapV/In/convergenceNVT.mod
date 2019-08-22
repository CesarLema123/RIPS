# This is the file which will be used to check that the system has converged to the right thermodynamic boundary conditions

# Specify where to write thermo data
log	log.loop

# Specify the number of steps bewteen convergence checks (must be a multiple of NLOOP)
variable NLOOP equal ${NFREQ} # variable from initConv.mod

# Specify how many times convergence must be met in a row before exitting
variable loopExit equal 3
variable i loop ${loopExit}


# Specify the percent change accpetable between standard deviations of thermo variables between checks for convergence
# (STD1 - STD0) < Err*STD1 is converged
variable tempErr equal 0.01
variable energyErr equal 0.01
variable pressErr equal 0.01
variable volumeErr equal 0.01

# variable to store previous std
variable energySTD1 equal 0.0
variable pressSTD1 equal 0.0
variable volumeSTD1 equal 0.0
variable tempSTD1 equal 0.0

label top

# run 
run ${NLOOP}
print "$i"

# check convergence of standard deviations
if "$(abs(v_energySTD-v_energySTD1)>(v_energyErr*v_energySTD1)) || $(abs(v_tempSTD-v_tempSTD1)>(v_tempErr*v_tempSTD1)) || $(abs(v_volumeSTD-v_volumeSTD1)>(v_volumeErr*v_volumeSTD1)) || $(abs(v_pressSTD-v_pressSTD1)>(v_pressErr*v_pressSTD1))" then &
	"variable i delete" &
	"variable i loop ${loopExit}" &
	"jump convergenceNVT.mod set_vars" 

# Part Specific to NVT: It must also be near the target temperature
if "$(abs(v_varAveTemp-v_TEMPERATURE)>v_absTempErr)" then &
	"variable i delete" &
	"variable i loop ${loopExit}" &
	"jump convergenceNVT.mod set_vars" 
	

# Check if converged enough times
if "$i < ${loopExit}" then "next i" "jump convergenceNVT.mod set_vars" else "jump convergenceNVT.mod break"

label set_vars

# update previous standard deviations before next run
variable energySTD1 equal $(v_energySTD)
variable pressSTD1 equal $(v_pressSTD)
variable volumeSTD1 equal $(v_volumeSTD)
variable tempSTD1 equal $(v_tempSTD)
jump convergenceNVT.mod top

label break


# Clean up convergence fixes 

unfix aveTemp
unfix aveTempSq
unfix aveEnergy
unfix aveEnergySq
unfix aveEnthalpy
unfix aveEnthalpySq
unfix avePress
unfix avePressSq
unfix aveVolume
unfix aveVolumeSq




