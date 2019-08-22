# This is the file which will be used to check that the system has converged to the right thermodynamic boundary conditions

# where to write the thermo-data during the loop
log	log.loop 
# variable from initConv.mod # NLOOP must be an integer multiple of NFREQ
variable NLOOP equal ${NFREQ} 
# Pass the convergence criteria this many times in a row before breaking loop
variable loopExit equal 3 
variable i loop ${loopExit}


# The difference between standard deviations variable *** between steps should be less that ***Err times ***STD to be converged
variable tempErr equal 0.01
variable energyErr equal 0.01
variable pressErr equal 0.01
variable volumeErr equal 0.01

# Initialize variables to hold old standard deviation results
variable energySTD1 equal 0.0
variable pressSTD1 equal 0.0
variable volumeSTD1 equal 0.0
variable tempSTD1 equal 0.0
label top

# run for some time
run ${NLOOP}

print "$i"

# check convergence criteria
if "$(abs(v_energySTD-v_energySTD1)>(v_energyErr*v_energySTD1)) || $(abs(v_tempSTD-v_tempSTD1)>(v_tempErr*v_tempSTD1)) || $(abs(v_volumeSTD-v_volumeSTD1)>(v_volumeErr*v_volumeSTD1)) || $(abs(v_pressSTD-v_pressSTD1)>(v_pressErr*v_pressSTD1))" then &
	"variable i delete" &
	"variable i loop ${loopExit}" &
	"jump convergenceNPT.mod set_vars" 

# Part Specific to NPT: It must also be near the target temperature and pressure
if "$(abs(v_varAveTemp-v_TEMPERATURE)>v_absTempErr) || $(abs(v_varAvePress-v_PRESSURE)>v_absPressErr)" then &
	"variable i delete" &
	"variable i loop ${loopExit}" &
	"jump convergenceNPT.mod set_vars" 
	
# Check if we've met the convergence criteria enough times
if "$i < ${loopExit}" then "next i" "jump convergenceNPT.mod set_vars" else "jump convergenceNPT.mod break"

# Update the previous std variable
label set_vars

variable energySTD1 equal $(v_energySTD)
variable pressSTD1 equal $(v_pressSTD)
variable volumeSTD1 equal $(v_volumeSTD)
variable tempSTD1 equal $(v_tempSTD)
jump convergenceNPT.mod top

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




