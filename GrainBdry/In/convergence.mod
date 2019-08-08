# This is the file which will be used to check that the system has converged to the right thermodynamic boundary conditions


log	log.loop
variable loopExit equal 3
variable i loop ${loopExit}



variable tempErr equal 0.01
variable energyErr equal 0.05
variable pressErr equal 0.05

variable energySTD1 equal 0.0
variable pressSTD1 equal 0.0
label top

run ${NLOOP}
print "$i"
print "$(abs(v_pressSTD - v_pressSTD1)) > $(v_pressErr*v_pressSTD1) || $(abs(v_energySTD - v_energySTD1)) > $(v_energyErr*v_energySTD1) ||  $(abs(v_varAveTemp - v_TEMPERATURE)) > $(v_tempErr*v_TEMPERATURE)"
if "$(abs(v_pressSTD - v_pressSTD1)) > $(v_pressErr*v_pressSTD1) || $(abs(v_energySTD - v_energySTD1)) > $(v_energyErr*v_energySTD1) ||  $(abs(v_varAveTemp - v_TEMPERATURE)) > $(v_tempErr*v_TEMPERATURE)" then "variable i loop ${loopExit}" "jump convergence.mod set_vars" 
if "$i < ${loopExit}" then "next i" "jump convergence.mod set_vars" else "jump convergence.mod break"

label set_vars

variable energySTD1 equal $(v_energySTD)
variable pressSTD1 equal $(v_pressSTD)
jump convergence.mod top

label break


