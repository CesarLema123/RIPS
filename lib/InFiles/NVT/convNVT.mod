
log			log.conv
variable		loopExit equal 3
variable		i loop ${loopExit}
variable  		saveEnergySTD equal 0.0
variable		savePressSTD equal 0.0


label 			loop

run 			${NCONV}


if "$(abs(v_saveEnergySTD-v_energySTD)>v_energyErr*v_saveEnergySTD) || $(abs(v_pressSTD-v_savePressSTD)>v_pressErr*v_savePressSTD) || $(abs(v_varAveTemp-v_TEMPERATURE)>v_tempErr*v_TEMPERATURE)" then "variable i loop ${loopExit}" "jump convNVT.mod setVars"
if "${i} < ${loopExit}" then "next i" "jump convNVT.mod setVars" else "jump convNVT.mod break"

label			setVars
variable saveEnergySTD equal $(v_energySTD)
variable savePressSTD equal $(v_pressSTD)
jump convNVT.mod loop

label			break

