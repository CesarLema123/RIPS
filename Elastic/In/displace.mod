# NOTE: This script should not need to be
# modified. See in.elastic for more info.
#
# Find which reference length to use

if "${dir} == 1" then &
   "variable len0 equal ${lx0}" 
if "${dir} == 2" then &
   "variable len0 equal ${ly0}" 
if "${dir} == 3" then &
   "variable len0 equal ${lz0}" 
if "${dir} == 4" then &
   "variable len0 equal ${lz0}" 
if "${dir} == 5" then &
   "variable len0 equal ${lz0}" 
if "${dir} == 6" then &
   "variable len0 equal ${ly0}" 

# Reset box and simulation parameters

clear
box tilt large
read_restart restart.equil
include potential.mod

# Negative deformation

variable delta equal -${up}*${len0}
variable deltaxy equal -${up}*xy
variable deltaxz equal -${up}*xz
variable deltayz equal -${up}*yz
if "${dir} == 1" then &
   "change_box all x delta 0 ${delta} xy delta ${deltaxy} xz delta ${deltaxz} remap units box"
if "${dir} == 2" then &
   "change_box all y delta 0 ${delta} yz delta ${deltayz} remap units box"
if "${dir} == 3" then &
   "change_box all z delta 0 ${delta} remap units box"
if "${dir} == 4" then &
   "change_box all yz delta ${delta} remap units box"
if "${dir} == 5" then &
   "change_box all xz delta ${delta} remap units box"
if "${dir} == 6" then &
   "change_box all xy delta ${delta} remap units box"

# Run MD
log.convNeg${dir}
include convergence.mod
log.runNeg${dir}
include potential.mod
run ${RUNTIME}

# Obtain new stress tensor
 
variable pxx1 equal v_varAvePxx
variable pyy1 equal v_varAvePyy
variable pzz1 equal v_varAvePzz
variable pxy1 equal v_varAvePxy
variable pxz1 equal v_varAvePxz
variable pyz1 equal v_varAvePyz

variable dpxx1 equal v_pxxSTD/sqrt(${RUNTIME}/${nevery})  # Using error based on standard deviation of the mean rather than standard deviation
variable dpyy1 equal v_pyySTD/sqrt(${RUNTIME}/${nevery})
variable dpzz1 equal v_pzzSTD/sqrt(${RUNTIME}/${nevery})
variable dpxy1 equal v_pxySTD/sqrt(${RUNTIME}/${nevery})
variable dpxz1 equal v_pxzSTD/sqrt(${RUNTIME}/${nevery})
variable dpyz1 equal v_pyzSTD/sqrt(${RUNTIME}/${nevery})





# Compute elastic constant from pressure tensor

variable C1neg equal ${d1}
variable C2neg equal ${d2}
variable C3neg equal ${d3}
variable C4neg equal ${d4}
variable C5neg equal ${d5}
variable C6neg equal ${d6}

variable dC1neg equal ${dd1}
variable dC2neg equal ${dd2}
variable dC3neg equal ${dd3}
variable dC4neg equal ${dd4}
variable dC5neg equal ${dd5}
variable dC6neg equal ${dd6}


# Reset box and simulation parameters

clear
box tilt large
read_restart restart.equil
include potential.mod

# Positive deformation

variable delta equal ${up}*${len0}
variable deltaxy equal ${up}*xy
variable deltaxz equal ${up}*xz
variable deltayz equal ${up}*yz
if "${dir} == 1" then &
   "change_box all x delta 0 ${delta} xy delta ${deltaxy} xz delta ${deltaxz} remap units box"
if "${dir} == 2" then &
   "change_box all y delta 0 ${delta} yz delta ${deltayz} remap units box"
if "${dir} == 3" then &
   "change_box all z delta 0 ${delta} remap units box"
if "${dir} == 4" then &
   "change_box all yz delta ${delta} remap units box"
if "${dir} == 5" then &
   "change_box all xz delta ${delta} remap units box"
if "${dir} == 6" then &
   "change_box all xy delta ${delta} remap units box"

# Run MD
log log.convPos${dir}
include convergence.mod

log log.runPos${dir}
include potential.mod
run ${RUNTIME}

# Obtain new stress tensor
 
variable tmp equal pe
variable e1 equal ${tmp}
variable tmp equal v_varAvePress
variable p1 equal ${tmp}
variable tmp equal v_varAvePxx
variable pxx1 equal ${tmp}
variable tmp equal v_varAvePyy
variable pyy1 equal ${tmp}
variable tmp equal v_varAvePzz
variable pzz1 equal ${tmp}
variable tmp equal v_varAvePxy
variable pxy1 equal ${tmp}
variable tmp equal v_varAvePxz
variable pxz1 equal ${tmp}
variable tmp equal v_varAvePyz
variable pyz1 equal ${tmp}

# Compute elastic constant from pressure tensor

variable C1pos equal ${d1}
variable C2pos equal ${d2}
variable C3pos equal ${d3}
variable C4pos equal ${d4}
variable C5pos equal ${d5}
variable C6pos equal ${d6}

variable dC1pos equal ${dd1}
variable dC2pos equal ${dd2}
variable dC3pos equal ${dd3}
variable dC4pos equal ${dd4}
variable dC5pos equal ${dd5}
variable dC6pos equal ${dd6}
# Combine positive and negative 

variable C1${dir} equal 0.5*(${C1neg}+${C1pos})
variable C2${dir} equal 0.5*(${C2neg}+${C2pos})
variable C3${dir} equal 0.5*(${C3neg}+${C3pos})
variable C4${dir} equal 0.5*(${C4neg}+${C4pos})
variable C5${dir} equal 0.5*(${C5neg}+${C5pos})
variable C6${dir} equal 0.5*(${C6neg}+${C6pos})

variable dC1${dir} equal 0.5*(${dC1neg}+${dC1pos})/sqrt(2) # Since C11 is an average, I quote 
variable dC2${dir} equal 0.5*(${dC2neg}+${dC2pos})/sqrt(2)
variable dC3${dir} equal 0.5*(${dC3neg}+${dC3pos})/sqrt(2)
variable dC4${dir} equal 0.5*(${dC4neg}+${dC4pos})/sqrt(2)
variable dC5${dir} equal 0.5*(${dC5neg}+${dC5pos})/sqrt(2)
variable dC6${dir} equal 0.5*(${dC6neg}+${dC6pos})/sqrt(2)



# Delete dir to make sure it is not reused

variable dir delete
