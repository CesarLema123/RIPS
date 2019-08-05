# NOTE: This script can be modified for different atomic structures, 
# units, etc. See in.elastic for more info.
#

# Define the finite deformation size. Try several values of this
# variable to verify that results do not depend on it.
variable up equal 2.0e-2
 
# metal units, elastic constants in GPa
units		metal
variable cfac equal 1.0e-4
variable cunits string GPa

# Define MD parameters
variable nevery equal 10                  # sampling interval
variable nrepeat equal 10                 # number of samples
variable nfreq equal ${nevery}*${nrepeat} # length of one average
variable nthermo equal ${nfreq}           # interval for thermo output
variable nequil equal 10*${nthermo}       # length of equilibration run
variable nrun equal 3*${nthermo}          # length of equilibrated run
variable TEMPERATURE equal 2000.0                # temperature of initial sample
variable TIMESTEP equal 0.001             # TIMESTEP
variable kT equal 10			# lammps manual suggests 100 but example set it to 10
variable tdamp equal ${kT}*${TIMESTEP}  # time constant for thermostat
variable RANDOM equal 123457                # seed for thermostat

# generate the box and atom positions
dimension 	3
boundary	p p p
atom_style 	atomic
read_data	data.elastic
