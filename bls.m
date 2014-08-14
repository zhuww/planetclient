function zz=bls(n,t,x,nf,fmini,df,nb,qmi,qma)
   y=zeros(1,2000);
   ibi=zeros(1,2000);
   p=zeros(1,nf);
   fff=zeros(1,nf);
   ddd=zeros(1,nf);
   junk1=size(t);
   u=zeros(1,junk1(1,2));
   v=zeros(1,junk1(1,2));

      minbin = 5;
      nbmax  = 2000;
      if(nb>nbmax)
          disp( ' NB > NBMAX !!')
      end
      if(nb>nbmax) 
          return
      end
      tot=t(n)-t(1);
      if(fmini<1/tot) 
         disp(' fmin < 1/T !!')
      end
      if(fmini<1/tot) 
          return
      end

      rn=n;
      kmi=floor(qmi*(nb));
      if(kmi<1)
          kmi=1;
      end
      kma=floor(qma*(nb))+1;
      kkmi=floor(rn*qmi);
      if(kkmi<minbin) 
          kkmi=minbin;
      end
      bpow=0;

      s=0;
      t1=t(1);
      for i=1:1:n
      u(i)=t(i)-t1;
      s=s+x(i);
      %sv=s
      %xv=x(i)
      end
      s=s/rn;
      %sv=s
      for i=1:1:n
      v(i)=x(i)-s;
      end

%uv=u
%vv=v
for jf=1:1:nf
      f0=fmini+df*(jf-1);
      p0=1/f0;
      fff(jf)=f0;
      ddd(jf)=p0;
     for j=1:1:nb
        y(j) = 0;
      ibi(j) = 0;
     end

      for i=1:1:n 
      ph=u(i)*f0;
      ph=ph-floor(ph);
      j=1+floor(nb*ph);
      ibi(j)=ibi(j)+1;
       y(j)=y(j)+v(i);
       %yv=y(j)
      end  




power=0;

      for i=1:1:nb
      s     = 0;
      k     = 0;
      kk    = 0;
      nb2   = i+kma;
      if(nb2>nb) 
          nb2=nb ;
      end
     for j=i:1:nb2
      k     = k+1;
      kk    = kk+ibi(j);%%%%%%%%%%%%%%%%%%%%%%%%%%
      s     = s+y(j);
      %sv=s
      if(k<kmi) 
          continue
      end
      if(kk<kkmi) 
          continue
      end
      rn1   = kk;
      %rnrn1=rn-rn1
      %sv=s
      pow   = s*s/(rn1*(rn-rn1));%abs
      %pow
      if((pow<power) )%&& (pow~=Inf)&&(pow~=NaN) 
          continue;
      end
      %rn-rn1
      power = pow;
      jn1   = i;
      jn2   = j;
      rn3   = rn1;
      s3    = s;
    end
      end
      %power
        power = sqrt(power);
      p(jf) = power;

      if(power<bpow) 
          continue
      end
      bpow  =  power;
      in1   =  jn1;
      in2   =  jn2;
      qtran =  rn3/rn;
      depth = -s3*rn/(rn3*(rn-rn3));
      bper  =  p0;

end
depth
plot(ddd,p,'*')
 %zz=p;
end
      
      
      