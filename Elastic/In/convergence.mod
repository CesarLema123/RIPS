# This is the file which will be used to check that the system has converged to the right thermodynamic boundary conditions

variable loopExit equal 3
variable i loop ${loopExit}


variable pxxErr equal 0.05
variable pyyErr equal 0.05
variable pzzErr equal 0.05
variable pxyErr equal 0.05
variable pxzErr equal 0.05
variable pyzErr equal 0.05

variable tempErr equal 0.01
variable energyErr equal 0.01

variable energySTD1 equal 0.0
variable pxxSTD1 equal 0.0
variable pyySTD1 equal 0.0
variable pzzSTD1 equal 0.0
variable pxySTD1 equal 0.0
variable pxzSTD1 equal 0.0
variable pyzSTD1 equal 0.0

label top

run ${nequil}
print "$(abs(v_pxxSTD - v_pxxSTD1)) > $(v_pxxErr*v_pxxSTD1) || $(abs(v_pyySTD - v_pyySTD1)) > $(v_pyyErr*v_pyySTD1) || $(abs(v_pzzSTD - v_pzzSTD1)) > $(v_pzzErr*v_pzzSTD1) || $(abs(v_pxySTD - v_pxySTD1)) > $(v_pxyErr*v_pxySTD1) || $(abs(v_pxzSTD - v_pxzSTD1)) > $(v_pxzErr*v_pxzSTD1) || $(abs(v_pyzSTD - v_pyzSTD1)) > $(v_pyzErr*v_pyzSTD1) || $(abs(v_energySTD - v_energySTD1)) > $(v_energyErr*v_energySTD1) || ${varAveTemp} > $(v_TEMPERATURE*(1 + v_energyErr)) || ${varAveTemp} < $(v_TEMPERATURE*(1-v_tempErr))" 
if "$(abs(v_pxxSTD - v_pxxSTD1)) > $(v_pxxErr*v_pxxSTD1) || $(abs(v_pyySTD - v_pyySTD1)) > $(v_pyyErr*v_pyySTD1) || $(abs(v_pzzSTD - v_pzzSTD1)) > $(v_pzzErr*v_pzzSTD1) || $(abs(v_pxySTD - v_pxySTD1)) > $(v_pxyErr*v_pxySTD1) || $(abs(v_pxzSTD - v_pxzSTD1)) > $(v_pxzErr*v_pxzSTD1) || $(abs(v_pyzSTD - v_pyzSTD1)) > $(v_pyzErr*v_pyzSTD1) || $(abs(v_energySTD - v_energySTD1)) > $(v_energyErr*v_energySTD1) || ${varAveTemp} > $(v_TEMPERATURE*(1 + v_energyErr)) || ${varAveTemp} < $(v_TEMPERATURE*(1-v_tempErr))" then "variable i loop ${loopExit}" "jump convergence.mod set_vars" 
if "$i < ${loopExit}" then "next i" "jump convergence.mod set_vars" else "jump convergence.mod break"



label set_vars

variable pxxSTD1 equal $(v_pxxSTD)
variable pyySTD1 equal $(v_pyySTD)
variable pzzSTD1 equal $(v_pzzSTD)
variable pxySTD1 equal $(v_pxySTD)
variable pxzSTD1 equal $(v_pxzSTD)
variable pyzSTD1 equal $(v_pyzSTD)
variable energySTD1 equal $(v_energySTD)
jump convergence.mod top

label break


