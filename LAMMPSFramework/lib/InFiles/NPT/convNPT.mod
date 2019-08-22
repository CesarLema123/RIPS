
log			log.conv
variable		loopExit equal 3
variable		i loop ${loopExit}
variable  		saveEnergySTD equal 0.0
variable		saveVolumeSTD equal 0.0


label loop

run 			${NCONV}


if "$(abs(v_saveEnergySTD-v_energySTD)>v_energyErr*v_saveEnergySTD) || $(abs(v_saveVolumeSTD-v_volumeSTD)>v_volumeErr*v_saveVolumeSTD) || $(abs(v_varAveTemp-v_TEMPERATURE))>${absTempErr} || $(abs(v_varAvePress-v_PRESSURE))>${absPressErr}" then "variable i loop ${loopExit}" "jump convNPT.mod setVars"
if "${i} < ${loopExit}" then "next i" "jump convNPT.mod setVars" else "jump convNPT.mod break"

label			setVars
variable saveEnergySTD equal $(v_energySTD)
variable saveVolumeSTD equal $(v_volumeSTD)
jump convNPT.mod loop

label			break

