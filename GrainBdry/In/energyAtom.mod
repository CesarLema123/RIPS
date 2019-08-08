variable	my_pe equal pe
variable	peSq equal "pe^2"
fix 		avePe all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_my_pe mode scalar ave window 20
fix 		avePeSq all ave/time ${NEVERY} ${NREPEAT} ${NFREQ} v_peSq mode scalar ave window 20
variable	peSTD equal "sqrt(abs(f_avePeSq - f_avePe^2))"
variable	varAvePe equal "f_avePe"

