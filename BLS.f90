!f2py -c -m BLS --f90flags="-lm " --opt="-O3 " --fcompiler=gnu95 BLS.f90 
!     
!     
      subroutine fbls(n,t,x,u,v,nf,fmin,df,nb,qmi,qma, &
                      p, pout)
!     
!c------------------------------------------------------------------------
!     >>>>>>>>>>>> This routine computes BLS spectrum <<<<<<<<<<<<<<
!     
!     [ see Kovacs, Zucker & Mazeh 2002, A&A, ... ]
!c------------------------------------------------------------------------
!     
!     Input parameters:
!     ~~~~~~~~~~~~~~~~~
!     
!     n    = number of data points
!     t    = array {t(i)}, containing the time values of the time series
!     x    = array {x(i)}, containing the data values of the time series
!     u    = temporal/work/dummy array, must be dimensioned in the 
!     calling program in the same way as  {t(i)}
!     v    = the same as  {u(i)}
!     nf   = number of frequency points in which the spectrum is computed
!     fmin = minimum frequency (MUST be > 0)
!     df   = frequency step
!     nb   = number of bins in the folded time series at any test period       
!     qmi  = minimum fractional transit length to be tested
!     qma  = maximum fractional transit length to be tested
!     
!     Output parameters:
!     ~~~~~~~~~~~~~~~~~~
!     
!     p    = array {p(i)}, containing the values of the BLS spectrum
!     at the i-th frequency value -- the frequency values are 
!     computed as  f = fmin + (i-1)*df
!     bper = period at the highest peak in the frequency spectrum
!     bpow = value of {p(i)} at the highest peak
!     depth= depth of the transit at   *bper*
!     qtran= fractional transit length  [ T_transit/bper ]
!     in1  = bin index at the start of the transit [ 0 < in1 < nb+1 ]
!     in2  = bin index at the end   of the transit [ 0 < in2 < nb+1 ]
!     
!     
!     Remarks:
!     ~~~~~~~~ 
!c
!     -- *fmin* MUST be greater than  *1/total time span* 
!     -- *nb*   MUST be lower than  *nbmax* 
!     -- Dimensions of arrays {y(i)} and {ibi(i)} MUST be greater than 
!     or equal to  *nbmax*. 
!     -- The lowest number of points allowed in a single bin is equal 
!     to   MAX(minbin,qmi*N),  where   *qmi*  is the minimum transit 
!     length/trial period,   *N*  is the total number of data points,  
!     *minbin*  is the preset minimum number of the data points per 
!     bin.
!     
!c========================================================================
!     
      implicit real*8 (a-h,o-z)
!     

      integer minbin

      dimension t(*),x(*),u(*),v(*),p(*), pout(*)
      dimension y(2000),ibi(2000)
      bper = 0
      bpow = 0 
      depth = 0 
      qtran = 0
      in1 = 0
      in2 = 0
      minbin = 5
      nbmax  = 2000
      if(nb.gt.nbmax) write(*,*) ' NB > NBMAX !!'
      if(nb.gt.nbmax) stop
      tot=t(n)-t(1)
      if(fmin.lt.1.0d0/tot) write(*,*) ' fmin < 1/T !!', 1./tot
      if(fmin.lt.1.0d0/tot) stop

!c------------------------------------------------------------------------
!     
      !write(*,*) 'here 2'
      
      rn=dfloat(n)
      kmi=idint(qmi*dfloat(nb))
      if(kmi.lt.1) kmi=1
      kma=idint(qma*dfloat(nb))+1
      kkmi=idint(rn*qmi)
      if(kkmi.lt.minbin) kkmi=minbin
      bpow = 0.0d0
      
!     
!c=================================
!     Set temporal time series
!c=================================
!     

      !write(*,*) 'here 3'

      s=0.0d0
      t1=t(1)
      do 103 i=1,n
         u(i)=t(i)-t1
         s=s+x(i)
 103  continue
      s=s/rn
      do 109 i=1,n
         v(i)=x(i)-s
 109  continue

!     
!c******************************
!     Start period search     *
!c******************************
!     
      
      !write(*,*) 'here 4'

      do 100 jf=1,nf
         f0=fmin+df*dfloat(jf-1)
         p0=1.0d0/f0
!     
!c======================================================
!     Compute folded time series with  *p0*  period
!c======================================================
!     
         do 101 j=1,nb
            y(j) = 0.0d0
            ibi(j) = 0
 101     continue
!     
         do 102 i=1,n
            ph     = u(i)*f0
             ph     = ph-idint(ph)
            j      = 1 + idint(nb*ph)
            ibi(j) = ibi(j) + 1
            y(j)  =   y(j) + v(i)
 102     continue



!     
!c===============================================
!     Compute BLS statistics for this period
!c===============================================
!     
      !write(*,*) 'here y'!, y
         
         power=0.0d0
         
         do 1 i=1,nb
            s     = 0.0d0
            k     = 0
            kk    = 0
            nb2   = i+kma
            if(nb2.gt.nb) nb2=nb
            do 2 j=i,nb2
               k     = k+1
               kk    = kk+ibi(j)
               s = s+y(j)
               if(k.lt.kmi) then
                  go to 2
               endif
               if(kk.lt.kkmi) then
                  go to 2
               endif
               rn1   = dfloat(kk)
               pow   = s*s/(rn1*(rn-rn1))
               if(pow.lt.power) go to 2
               power = pow
               jn1   = i
               jn2   = j
               rn3   = rn1
               s3    = s
 2          continue
 1       continue
!     
         power = dsqrt(power)
         p(jf) = power
        !write(*,*) 'power', power
!     
         if(power.lt.bpow) then
            go to 100
         endif
         bpow  =  power         
         in1   =  jn1
         in2   =  jn2
         qtran =  rn3/rn
         depth = -s3*rn/(rn3*(rn-rn3))
         bper  =  p0
!     
 100  continue

      pout(1) = bper
      pout(2) = bpow
      pout(3) = depth
      pout(4) = qtran
      pout(5) = in1
      pout(6) = in2
!     
      return 
      end
!     
!     
!!$
