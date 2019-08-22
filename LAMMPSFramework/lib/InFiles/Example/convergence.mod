# This is the file which will be used to check that the system has converged to the right thermodynamic boundary conditions


log	log.loop
variable NLOOP equal ${NFREQ} # variable from initConv.mod
variable loopExit equal 3
variable i loop ${loopExit}



variable tempErr equal 0.01
variable energyErr equal 0.01
variable pressErr equal 0.01
variable volumeErr equal 0.01

variable energySTD1 equal 0.0
variable pressSTD1 equal 0.0
variable volumeSTD1 equal 0.0
variable tempSTD1 equal 0.0
label top

run ${NLOOP}
print "$i"
if "$(abs(v_energySTD-v_energySTD1)>(v_energyErr*v_energySTD1)) || $(abs(v_tempSTD-v_tempSTD1)>(v_tempErr*v_tempSTD1)) || $(abs(v_volumeSTD-v_volumeSTD1)>(v_volumeErr*v_volumeSTD1)) || $(abs(v_pressSTD-v_pressSTD1)>(v_pressErr*v_pressSTD1))" then &
	"variable i delete" &
	"variable i loop ${loopExit}" &
	"jump convergence.mod set_vars" 
if "$i < ${loopExit}" then "next i" "jump convergence.mod set_vars" else "jump convergence.mod break"

label set_vars

variable energySTD1 equal $(v_energySTD)
variable pressSTD1 equal $(v_pressSTD)
variable volumeSTD1 equal $(v_volumeSTD)
variable tempSTD1 equal $(v_tempSTD)
jump convergence.mod top

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




