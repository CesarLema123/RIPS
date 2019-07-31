#!/bin/bash

# This is a template of the submission file which can be copied 
# and used for different jobs










. /u/local/Modules/default/init/modules.sh
module load python/3.7.2

export MY_PYTHON_LIB=$HOME"/travis/lib/PyScripts"
export MY_AWK_LIB=$HOME"/travis/lib/AwkFiles"
export MY_CURRENT_DIR=$HOME"/travis/NPTSIM"
export MY_LAMMPS="lammps.q"


cd $MY_CURRENT_DIR

# ------------ WRITING THE IN AND DATA FILES ----------
for runTime in 1000; # fs
do
for numAtoms in 8;
do
for temp in  {100..2500..100};
do
for press in 0; #{-100..100..10};
do
for concInt in 3; #{0..10..1};
do

# Making the directory to store files for the particular run
export workDir="RunTime"$runTime"NumAtoms"$numAtoms"ConcInt"$concInt"Temp"$temp"Press"$press
mkdir "Out/"$workDir

# copying relavent files to this directory
cp in.Template CuNi.eam.alloy "Out/"$workDir
cd "Out/"$workDir

# Making the initial donfiguration file
python3 $MY_PYTHON_LIB/writeData.py $numAtoms $concInt

# Making the in file lammps will read from the template
python3 $MY_PYTHON_LIB/writeInCuNiNPT.py $runTime $numAtoms $concInt $temp $press

# Running lammps
$MY_LAMMPS in.CuNi

sleep 10

# Going back to main directory
cd $MY_CURRENT_DIR 

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
