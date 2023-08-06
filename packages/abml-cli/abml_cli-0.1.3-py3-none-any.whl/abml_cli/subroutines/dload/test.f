subroutine DLOAD(F,KSTEP,KINC,TIME,NOEL,NPT,LAYER,KSPT,
     &                 COORDS,JLTYP,SNAME)
C
      include 'ABA_PARAM.INC'
C
      dimension TIME(2), COORDS(3)
      CHARACTER*80 SNAME
C
      X=COORDS(1)
      Y=COORDS(2)
      Z=COORDS(3)
C
      else if (sqrt((x-(10))**2+(y-(20))**2)<10) then
        F = 20
      else
        F = 0.0
      endif
    

      RETURN
      END