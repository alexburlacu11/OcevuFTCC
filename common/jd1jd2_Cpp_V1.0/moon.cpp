#include "moon.h"
//------------------------------------------------------------------------------
// Constructor
Moon::Moon()
{
}
//------------------------------------------------------------------------------
// Destructor
Moon::~Moon()
{
}

//------------------------------------------------------------------------------
// More accurate (but more elaborate and slower) lunar ephemeris
//   from Jean Meeus' *Astronomical Formulae For Calculators,
//   pub. Willman-Bell.  Includes all the terms given there.
// inputs units:geolat in decimal degrees, lst in decimal hours., elevsea in meters
void Moon::accumoon( double JD, double geolat, double lst, double elevsea, Moon *moon)
{
  Astronomy *astro = new Astronomy;
  double jd = JD + astro->etcorr(JD)/SEC_IN_DAY;   // approximate correction to ephemeris time
  double T = (jd - 2415020.) / 36525.;   // this based around 1900 ...
  double Tsq = T * T;
  double Tcb = Tsq * T;

  double Lpr = 270.434164 + 481267.8831 * T - 0.001133 * Tsq + 0.0000019 * Tcb;
  double M = 358.475833 + 35999.0498*T - 0.000150*Tsq - 0.0000033*Tcb;
  double Mpr = 296.104608 + 477198.8491*T + 0.009192*Tsq + 0.0000144*Tcb;
  double D = 350.737486 + 445267.1142*T - 0.001436 * Tsq + 0.0000019*Tcb;
  double F = 11.250889 + 483202.0251*T -0.003211 * Tsq - 0.0000003*Tcb;
  double Om = 259.183275 - 1934.1420*T + 0.002078*Tsq + 0.0000022*Tcb;

  Lpr = astro->circulo(Lpr);
  Mpr = astro->circulo(Mpr);
  M = astro->circulo(M);
  D = astro->circulo(D);
  F = astro->circulo(F);
  Om = astro->circulo(Om);


  double sinx =  sin((51.2 + 20.2 * T)/DEG_IN_RADIAN);
  Lpr = Lpr + 0.000233 * sinx;
  M = M - 0.001778 * sinx;
  Mpr = Mpr + 0.000817 * sinx;
  D = D + 0.002011 * sinx;

  sinx = 0.003964 * sin((346.560+132.870*T -0.0091731*Tsq)/DEG_IN_RADIAN);

  Lpr = Lpr + sinx;
  Mpr = Mpr + sinx;
  D = D + sinx;
  F = F + sinx;


  sinx = sin(Om/DEG_IN_RADIAN);
  Lpr = Lpr + 0.001964 * sinx;
  Mpr = Mpr + 0.002541 * sinx;
  D = D + 0.001964 * sinx;
  F = F - 0.024691 * sinx;
  F = F - 0.004328 * sin((Om + 275.05 -2.30*T)/DEG_IN_RADIAN);

  double e = 1 - 0.002495 * T - 0.00000752 * Tsq;

  M = M / DEG_IN_RADIAN;   // these will all be arguments ...
  Mpr = Mpr / DEG_IN_RADIAN;
  D = D / DEG_IN_RADIAN;
  F = F / DEG_IN_RADIAN;

  double lambda = Lpr + 6.288750 * sin(Mpr)
  + 1.274018 * sin(2*D - Mpr)
  + 0.658309 * sin(2*D)
  + 0.213616 * sin(2*Mpr)
  - e * 0.185596 * sin(M)
  - 0.114336 * sin(2*F)
  + 0.058793 * sin(2*D - 2*Mpr)
  + e * 0.057212 * sin(2*D - M - Mpr)
  + 0.053320 * sin(2*D + Mpr)
  + e * 0.045874 * sin(2*D - M)
  + e * 0.041024 * sin(Mpr - M)
  - 0.034718 * sin(D)
  - e * 0.030465 * sin(M+Mpr)
  + 0.015326 * sin(2*D - 2*F)
  - 0.012528 * sin(2*F + Mpr)
  - 0.010980 * sin(2*F - Mpr)
  + 0.010674 * sin(4*D - Mpr)
  + 0.010034 * sin(3*Mpr)
  + 0.008548 * sin(4*D - 2*Mpr)
  - e * 0.007910 * sin(M - Mpr + 2*D)
  - e * 0.006783 * sin(2*D + M)
  + 0.005162 * sin(Mpr - D);

  // And furthermore.....

  lambda = lambda + e * 0.005000 * sin(M + D)
  + e * 0.004049 * sin(Mpr - M + 2*D)
  + 0.003996 * sin(2*Mpr + 2*D)
  + 0.003862 * sin(4*D)
  + 0.003665 * sin(2*D - 3*Mpr)
  + e * 0.002695 * sin(2*Mpr - M)
  + 0.002602 * sin(Mpr - 2*F - 2*D)
  + e * 0.002396 * sin(2*D - M - 2*Mpr)
  - 0.002349 * sin(Mpr + D)
  + e * e * 0.002249 * sin(2*D - 2*M)
  - e * 0.002125 * sin(2*Mpr + M)
  - e * e * 0.002079 * sin(2*M)
  + e * e * 0.002059 * sin(2*D - Mpr - 2*M)
  - 0.001773 * sin(Mpr + 2*D - 2*F)
  - 0.001595 * sin(2*F + 2*D)
  + e * 0.001220 * sin(4*D - M - Mpr)
  - 0.001110 * sin(2*Mpr + 2*F)
  + 0.000892 * sin(Mpr - 3*D)
  - e * 0.000811 * sin(M + Mpr + 2*D)
  + e * 0.000761 * sin(4*D - M - 2*Mpr)
  + e * e * 0.000717 * sin(Mpr - 2*M)
  + e * e * 0.000704 * sin(Mpr - 2 * M - 2*D)
  + e * 0.000693 * sin(M - 2*Mpr + 2*D)
  + e * 0.000598 * sin(2*D - M - 2*F)
  + 0.000550 * sin(Mpr + 4*D)
  + 0.000538 * sin(4*Mpr)
  + e * 0.000521 * sin(4*D - M)
  + 0.000486 * sin(2*Mpr - D);

  //    eclongit = lambda;

  double B = 5.128189 * sin(F)
  + 0.280606 * sin(Mpr + F)
  + 0.277693 * sin(Mpr - F)
  + 0.173238 * sin(2*D - F)
  + 0.055413 * sin(2*D + F - Mpr)
  + 0.046272 * sin(2*D - F - Mpr)
  + 0.032573 * sin(2*D + F)
  + 0.017198 * sin(2*Mpr + F)
  + 0.009267 * sin(2*D + Mpr - F)
  + 0.008823 * sin(2*Mpr - F)
  + e * 0.008247 * sin(2*D - M - F)
  + 0.004323 * sin(2*D - F - 2*Mpr)
  + 0.004200 * sin(2*D + F + Mpr)
  + e * 0.003372 * sin(F - M - 2*D)
  + 0.002472 * sin(2*D + F - M - Mpr)
  + e * 0.002222 * sin(2*D + F - M)
  + e * 0.002072 * sin(2*D - F - M - Mpr)
  + e * 0.001877 * sin(F - M + Mpr)
  + 0.001828 * sin(4*D - F - Mpr)
  - e * 0.001803 * sin(F + M)
  - 0.001750 * sin(3*F)
  + e * 0.001570 * sin(Mpr - M - F)
  - 0.001487 * sin(F + D)
  - e * 0.001481 * sin(F + M + Mpr)
  + e * 0.001417 * sin(F - M - Mpr)
  + e * 0.001350 * sin(F - M)
  + 0.001330 * sin(F - D)
  + 0.001106 * sin(F + 3*Mpr)
  + 0.001020 * sin(4*D - F)
  + 0.000833 * sin(F + 4*D - Mpr);
  // not only that, but
  B = B + 0.000781 * sin(Mpr - 3*F)
  + 0.000670 * sin(F + 4*D - 2*Mpr)
  + 0.000606 * sin(2*D - 3*F)
  + 0.000597 * sin(2*D + 2*Mpr - F)
  + e * 0.000492 * sin(2*D + Mpr - M - F)
  + 0.000450 * sin(2*Mpr - F - 2*D)
  + 0.000439 * sin(3*Mpr - F)
  + 0.000423 * sin(F + 2*D + 2*Mpr)
  + 0.000422 * sin(2*D - F - 3*Mpr)
  - e * 0.000367 * sin(M + F + 2*D - Mpr)
  - e * 0.000353 * sin(M + F + 2*D)
  + 0.000331 * sin(F + 4*D)
  + e * 0.000317 * sin(2*D + F - M + Mpr)
  + e * e * 0.000306 * sin(2*D - 2*M - F)
  - 0.000283 * sin(Mpr + 3*F);


  double om1 = 0.0004664 * cos(Om/DEG_IN_RADIAN);
  double om2 = 0.0000754 * cos((Om + 275.05 - 2.30*T)/DEG_IN_RADIAN);

  double beta = B * (1. - om1 - om2);
  //      eclatit = beta;

  double pie = 0.950724
  + 0.051818 * cos(Mpr)
  + 0.009531 * cos(2*D - Mpr)
  + 0.007843 * cos(2*D)
  + 0.002824 * cos(2*Mpr)
  + 0.000857 * cos(2*D + Mpr)
  + e * 0.000533 * cos(2*D - M)
  + e * 0.000401 * cos(2*D - M - Mpr)
  + e * 0.000320 * cos(Mpr - M)
  - 0.000271 * cos(D)
  - e * 0.000264 * cos(M + Mpr)
  - 0.000198 * cos(2*F - Mpr)
  + 0.000173 * cos(3*Mpr)
  + 0.000167 * cos(4*D - Mpr)
  - e * 0.000111 * cos(M)
  + 0.000103 * cos(4*D - 2*Mpr)
  - 0.000084 * cos(2*Mpr - 2*D)
  - e * 0.000083 * cos(2*D + M)
  + 0.000079 * cos(2*D + 2*Mpr)
  + 0.000072 * cos(4*D)
  + e * 0.000064 * cos(2*D - M + Mpr)
  - e * 0.000063 * cos(2*D + M - Mpr)
  + e * 0.000041 * cos(M + D)
  + e * 0.000035 * cos(2*Mpr - M)
  - 0.000033 * cos(3*Mpr - 2*D)
  - 0.000030 * cos(Mpr + D)
  - 0.000029 * cos(2*F - 2*D)
  - e * 0.000029 * cos(2*Mpr + M)
  + e * e * 0.000026 * cos(2*D - 2*M)
  - 0.000023 * cos(2*F - 2*D + Mpr)
  + e * 0.000019 * cos(4*D - M - Mpr);

  beta = beta/DEG_IN_RADIAN;
  lambda = lambda/DEG_IN_RADIAN;
  double l = cos(lambda) * cos(beta);
  double m = sin(lambda) * cos(beta);
  double n = sin(beta);
  astro->eclrot(jd,&l,&m,&n);

  double dist = 1/sin((pie)/DEG_IN_RADIAN);
  double x = l * dist;
  double y = m * dist;
  double z = n * dist;

  moon->geora = astro->atan_circ(l,m) * HRS_IN_RADIAN;
  moon->geodec = asin(n) * DEG_IN_RADIAN;
  moon->geodist = dist;

  double x_geo, y_geo, z_geo;  // geocentric position of *observer*
  astro->geocent(lst,geolat,elevsea,&x_geo,&y_geo,&z_geo);

  x = x - x_geo;  // topocentric correction using elliptical earth fig.
  y = y - y_geo;
  z = z - z_geo;

  moon->topodist = sqrt(x*x + y*y + z*z);

  l = x / (moon->topodist);
  m = y / (moon->topodist);
  n = z / (moon->topodist);

  moon->topora = astro->atan_circ(l,m) * HRS_IN_RADIAN;
  moon->topodec = asin(n) * DEG_IN_RADIAN;

  delete astro;
}
//------------------------------------------------------------------------------
// Gives jd (+- 2 min) of phase nph on lunation n;
// This routine implements formulae found in Jean Meeus' *Astronomical Formulae
// for Calculators*, 2nd edition, Willman-Bell. A very useful book!!
// n, nph lunation and phase; nph = 0 new, 1 1st, 2 full, 3 last
// jdout   jd of requested phase
void Moon::flmoon( int n, int nph, double *jdout)
{
   double cor;
   double lun = (double) n + (double) nph / 4.;
   double T = lun / 1236.85;
   double jd = 2415020.75933 + 29.53058868 * lun
      + 0.0001178 * T * T
      - 0.000000155 * T * T * T
      + 0.00033 * sin((166.56 + 132.87 * T - 0.009173 * T * T)/DEG_IN_RADIAN);
   double M = 359.2242 + 29.10535608 * lun - 0.0000333 * T * T - 0.00000347 * T * T * T;
   M = M / DEG_IN_RADIAN;
   double Mpr = 306.0253 + 385.81691806 * lun + 0.0107306 * T * T + 0.00001236 * T * T * T;
   Mpr = Mpr / DEG_IN_RADIAN;
   double F = 21.2964 + 390.67050646 * lun - 0.0016528 * T * T - 0.00000239 * T * T * T;
   F = F / DEG_IN_RADIAN;
   if((nph == 0) || (nph == 2)) {// new or full
      cor =   (0.1734 - 0.000393*T) * sin(M)
         + 0.0021 * sin(2*M)
         - 0.4068 * sin(Mpr)
         + 0.0161 * sin(2*Mpr)
         - 0.0004 * sin(3*Mpr)
         + 0.0104 * sin(2*F)
         - 0.0051 * sin(M + Mpr)
         - 0.0074 * sin(M - Mpr)
         + 0.0004 * sin(2*F+M)
         - 0.0004 * sin(2*F-M)
         - 0.0006 * sin(2*F+Mpr)
         + 0.0010 * sin(2*F-Mpr)
         + 0.0005 * sin(M+2*Mpr);
      jd = jd + cor;
   }
   else {
      cor = (0.1721 - 0.0004*T) * sin(M)
         + 0.0021 * sin(2 * M)
         - 0.6280 * sin(Mpr)
         + 0.0089 * sin(2 * Mpr)
         - 0.0004 * sin(3 * Mpr)
         + 0.0079 * sin(2*F)
         - 0.0119 * sin(M + Mpr)
         - 0.0047 * sin(M - Mpr)
         + 0.0003 * sin(2 * F + M)
         - 0.0004 * sin(2 * F - M)
         - 0.0006 * sin(2 * F + Mpr)
         + 0.0021 * sin(2 * F - Mpr)
         + 0.0003 * sin(M + 2 * Mpr)
         + 0.0004 * sin(M - 2 * Mpr)
         - 0.0003 * sin(2*M + Mpr);
      if(nph == 1) cor = cor + 0.0028 -
            0.0004 * cos(M) + 0.0003 * cos(Mpr);
      if(nph == 3) cor = cor - 0.0028 +
            0.0004 * cos(M) - 0.0003 * cos(Mpr);
      jd = jd + cor;

   }
   *jdout = jd;
}
//------------------------------------------------------------------------------
// Compute age in days of moon since last new, and lunation of last new moon.
float Moon::lun_age( double jd,  int *nlun)
{
   double newjd, lastnewjd;
   short kount=0;
   float x;

   int nlast = (jd - 2415020.5) / 29.5307 - 1;

   flmoon(nlast,0,&lastnewjd);
   nlast++;
   flmoon(nlast,0,&newjd);
   while((newjd < jd) && (kount < 40))
   {
      lastnewjd = newjd;
      nlast++;
      flmoon(nlast,0,&newjd);
   }
   if(kount > 35)
   {
      cout << "Didn't find phase in lun_age!\n" << endl;
      x = -10.;
      *nlun = 0;
   }
   else
   {
     x = jd - lastnewjd;
     *nlun = nlast - 1;
   }

   return(x);
}
//------------------------------------------------------------------------------
// Prints a verbal description of moon phase, given the julian date.
string Moon::print_phase( double jd)
{
   ostringstream oss;
   string str="";

   double newjd, lastnewjd;
   double fqjd, fljd, lqjd;  // jds of first, full, and last in this lun.
   short kount=0;
   float x;

   int nlast = (jd - 2415020.5) / 29.5307 - 1;  // find current lunation

   flmoon(nlast,0,&lastnewjd);
   nlast++;
   flmoon(nlast,0,&newjd);
   while((newjd < jd) && (kount < 40))
   {
      lastnewjd = newjd;
      nlast++;
      flmoon(nlast,0,&newjd);
   }
   if(kount > 35)   // oops ... didn't find it ...
   {
      cout << "Didn't find phase in print_phase!\n" << endl;
      x = -10.;
   }
   else {     // found lunation ok
      x = jd - lastnewjd;
      nlast--;
      int noctiles = x / 3.69134;  // 3.69134 = 1/8 month; truncate.
      if(noctiles == 0)
         oss << fixed  << setprecision (2) << x << " days since new moon";
      else if (noctiles <= 2)  // nearest first quarter
      {
         flmoon(nlast,1,&fqjd);
         x = jd - fqjd;
         if(x < 0.)
           oss << fixed  << setprecision (2) << -1.*x << " days before first quarter";
         else
           oss << x << " days since first quarter";
      }
      else if (noctiles <= 4)  // nearest full
      {
         flmoon(nlast,2,&fljd);
         x = jd - fljd;
         if(x < 0.)
           oss << fixed  << setprecision (2) << -1.*x << " days until full moon";
         else
           oss << fixed  << setprecision (2) << x << " days after full moon";
      }
      else if (noctiles <= 6)  // nearest last quarter
      {
         flmoon(nlast,3,&lqjd);
         x = jd - lqjd;
         if(x < 0.)
           oss << fixed  << setprecision (2) << -1.*x << " days before last quarter";
         else
           oss << fixed  << setprecision (2) << x << " days after last quarter";
      }
      else oss << (newjd - jd) << " days before new moon";
      str=oss.str();
   }

   return str;
}
//------------------------------------------------------------------------------
// Implemenataion of Jean Meeus' more accurate solar ephemeris.
// For ultimate use in helio correction!
// From Astronomical Formulae for Calculators, pp. 79 ff.
// This gives sun's position wrt *mean* equinox of date, not *apparent*.
// Accuracy is << 1 arcmin.  Positions given are geocentric.
// Parallax due to observer's position on earth is ignored. This is up to
// 8 arcsec; Routine is usually a little better than that.
//      // -- topocentric correction *is* included now. -- //
// Light travel time is apparently taken into account for the ra and dec, but
// the author don't know if aberration is and he don't know if distance is
// simlarly antedated.
//
// x, y, and z are heliocentric equatorial coordinates of the
// EARTH, referred to mean equator and equinox of date.

double Moon::lunskybright(  double alpha,  double rho,  double kzen,  double altmoon,  double alt,   double moondist)
{
   double rho_rad = rho/DEG_IN_RADIAN;
   double alph = (180. - alpha);
   double Zmoon = (90. - altmoon)/DEG_IN_RADIAN;
   double Z = (90. - alt)/DEG_IN_RADIAN;
   double mndst = moondist/(60.27);  // divide by mean distance

   double istar = -0.4*(3.84 + 0.026*fabs(alph) + 4.0e-9*pow(alph,4.)); //eqn 20
   istar =  pow(10.,istar)/(mndst * mndst);
   if(fabs(alph) < 7.)   // crude accounting for opposition effect
      istar = istar * (1.35 - 0.05 * fabs(istar));
   // 35 per cent brighter at full, effect tapering linearly to zero at 7 degrees
   // away from full. mentioned peripherally in Krisciunas and Scheafer, p. 1035.
   double fofrho = 229087. * (1.06 + cos(rho_rad)*cos(rho_rad));
   if(fabs(rho) > 10.)
       fofrho=fofrho+pow(10.,(6.15 - rho/40.));            // eqn 21
   else if (fabs(rho) > 0.25)
       fofrho= fofrho+ 6.2e7 / (rho*rho);   // eqn 19
   else
       fofrho = fofrho+9.9e8;  //for 1/4 degree -- radius of moon!
   double Xzm = sqrt(1.0 - 0.96*sin(Zmoon)*sin(Zmoon));
   if(Xzm != 0.)
      Xzm = 1./Xzm;
   else
      Xzm = 10000.;
   double Xo = sqrt(1.0 - 0.96*sin(Z)*sin(Z));
   if(Xo != 0.)
      Xo = 1./Xo;
   else
      Xo = 10000.;
   double Bmoon = fofrho * istar * pow(10.,(-0.4*kzen*Xzm)) * (1. - pow(10.,(-0.4*kzen*Xo)));   // nanoLamberts
   if(Bmoon > 0.001)
      return(22.50 - 1.08574 * log(Bmoon/34.08)); // V mag per sq arcs-eqn 1
   else
      return(99.);
}
//------------------------------------------------------------------------------
// Returns jd at which moon is at a given altitude,
// given jdguess as a starting point. In current version uses high-precision
// moon -- execution time does not seem to be excessive on modern hardware.
// If it's a problem on your machine, you can replace calls to 'accumoon' with
// 'lpmoon' and remove the 'elevsea' argument.
double Moon::jd_moon_alt( double alt, double jdguess, double lat, double longit, double elevsea)
{
   Astronomy *astro = new Astronomy;
   Moon *moon = new Moon;
   double del = 0.002;
   double alt2,alt3,az,par;

   double sid=astro->lst(jdguess,longit);
   accumoon(jdguess,lat,sid,elevsea,moon);
   double ha = astro->lst(jdguess,longit) - moon->topora;
   astro->horizCoord(moon->topodec,ha,lat,&alt2,&az,&par);
   jdguess = jdguess + del;
   sid = astro->lst(jdguess,longit);
   accumoon(jdguess,lat,sid,elevsea,moon);
   astro->horizCoord(moon->topodec,(sid - moon->topora),lat,&alt3,&az,&par);
   double err = alt3 - alt;
   double deriv = (alt3 - alt2) / del;
   short i = 0;
   while((fabs(err) > 0.1) && (i < 10))
   {
      jdguess = jdguess - err/deriv;
      sid=astro->lst(jdguess,longit);
      accumoon(jdguess,lat,sid,elevsea,moon);
      astro->horizCoord(moon->topodec,(sid - moon->topora),lat,&alt3,&az,&par);
      err = alt3 - alt;
      i++;
      if(i == 9) cout << "Moonrise or -set calculation not converging!!" << endl;
   }
   if(i >= 9) jdguess = -1000.;
   double jdout = jdguess;
   delete astro;
   return(jdout);
}

//------------------------------------------------------------------------------
