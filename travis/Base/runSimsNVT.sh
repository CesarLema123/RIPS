#!/bin/bash

# This is a template of the submission file which can be copied 
# and used for different jobs










#. /u/local/Modules/default/init/modules.sh
#module load python/3.7.2

export MY_PYTHON_LIB=$HOME"/travis/lib/PyScripts"
export MY_AWK_LIB=$HOME"/travis/lib/AwkFiles"


cd $HOME"/travis/CuNiDiff"

# ------------ WRITING THE IN AND DATA FILES ----------
for runTime in 100; # fs
do
for numAtoms in 3;
do
for temp in 1900;
do
for length in "21.6";
do
for concInt in 3;
do

# Making the directory to store files for the particular run
export workDir="RunTime"$runTime"NumAtoms"$numAtoms"ConcInt"$concInt"Temp"$temp"Length"$length
mkdir "Out/"$workDir

# copying relavent files to this directory
cp in.Template CuNi.eam.alloy "Out/"$workDir
cd "Out/"$workDir

# Making the initial donfiguration file
python3 $MY_PYTHON_LIB/writeData.py $numAtoms $concInt

# Making the in file lammps will read from the template
python3 $MY_PYTHON_LIB/writeInCuNiDiff.py $runTime $numAtoms $concInt $temp $length

# Running lammps
lmp_daily -in in.CuNiDiff

# Editting the log files to be readable by pandas
awk -f $MY_AWK_LIB"/awkReadLog" log.run > log.data
awk -f $MY_AWK_LIB"/awkReadLog" log.loop > log.temp
awk -f $MY_AWK_LIB"/awkCombineLog" log.temp > log.loop


# Editing the dump file to have the write atom ids
awk -f $MY_AWK_LIB"/awkFixElementIdCuNi" dump.xyz > dump.pos
# Removing unneeded and duplicate files
rm -f log.run log.temp dump.xyz in.Template CuNi.eam.alloy

# Going back to main directory
cd $HOME"/travis/CuNiDiff"

done 
done
done 
done
done











#python3.6 [scriptname].py

# once you finish you should make your sh file into a cmd file by running

# "job.q -ns [scriptname].sh"

# Then change line 21 from "#$ -l h_data=1024M,h_rt=8:00:00" to
# "#$ -l h_data=[mempercore],h_rt=[runtime hh:mm:ss] -pe shared [numcores]"

# further edit the job to recieve emails upon completion
# line 28 command = -m [bean] b: begins e:ends a:aborts n:none

# Run the job using 
# qsub [scriptname].sh.cmd 

# check the job queue using qstat
# specifically "qstat -u $USER"


# upon beginning the system will create two files for a log and output

# delete a job using "qdel [jobid]"
