#include "sun.h"
//------------------------------------------------------------------------------
// Constructor
Sun::Sun()
{
}
//------------------------------------------------------------------------------
// Destructor
Sun::~Sun()
{
}

//------------------------------------------------------------------------------
// Low precision formulae for the sun, from Almanac p. C24 (1990)
// ra and dec are returned as decimal hours and decimal degrees.
void Sun::lpsun( double jd, double *ra, double *dec)
{
   Astronomy *astro = new Astronomy;
   double n = jd - J2000;
   double L = 280.460 + 0.9856474 * n;
   double g = (357.528 + 0.9856003 * n)/DEG_IN_RADIAN;
   double lambda = (L + 1.915 * sin(g) + 0.020 * sin(2. * g))/DEG_IN_RADIAN;
   double epsilon = (23.439 - 0.0000004 * n)/DEG_IN_RADIAN;

   double x = cos(lambda);
   double y = cos(epsilon) * sin(lambda);
   double z = sin(epsilon)*sin(lambda);

   *ra = (astro->atan_circ(x,y))*HRS_IN_RADIAN;
   *dec = (asin(z))*DEG_IN_RADIAN;

   delete astro;
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
void Sun::accusun( double JD, double lst, double geolat, Sun *sun)
{
  Astronomy *astro = new Astronomy;
  double xgeo, ygeo, zgeo;
  double x, y, z;

  double jd = JD + astro->etcorr(JD)/SEC_IN_DAY;  // might as well do it right ....
  double T = (jd - 2415020.) / 36525.;  // 1900 --- this is an oldish theory
  double Tsq = T*T;
  double Tcb = T*Tsq;
  double L = 279.69668 + 36000.76892*T + 0.0003025*Tsq;
  double M = 358.47583 + 35999.04975*T - 0.000150*Tsq - 0.0000033*Tcb;
  double e = 0.01675104 - 0.0000418*T - 0.000000126*Tsq;

  L = astro->circulo(L);
  M = astro->circulo(M);
  //      printf("raw L, M: %15.8f, %15.8f\n",L,M);

  double A = 153.23 + 22518.7541 * T;  // A, B due to Venus
  double B = 216.57 + 45037.5082 * T;
  double C = 312.69 + 32964.3577 * T;  // C due to Jupiter
  // D -- rough correction from earth-moon barycenter to center of earth.
  double D = 350.74 + 445267.1142*T - 0.00144*Tsq;
  double E = 231.19 + 20.20*T;    // "inequality of long period ..
  double H = 353.40 + 65928.7155*T;  // Jupiter.

  A = astro->circulo(A) / DEG_IN_RADIAN;
  B = astro->circulo(B) / DEG_IN_RADIAN;
  C = astro->circulo(C) / DEG_IN_RADIAN;
  D = astro->circulo(D) / DEG_IN_RADIAN;
  E = astro->circulo(E) / DEG_IN_RADIAN;
  H = astro->circulo(H) / DEG_IN_RADIAN;

  L = L + 0.00134 * cos(A)
  + 0.00154 * cos(B)
  + 0.00200 * cos(C)
  + 0.00179 * sin(D)
  + 0.00178 * sin(E);

  //   double Lrad = L/DEG_IN_RADIAN;
  double Mrad = M/DEG_IN_RADIAN;

  double Cent = (1.919460 - 0.004789*T -0.000014*Tsq)*sin(Mrad)
  + (0.020094 - 0.000100*T) * sin(2.0*Mrad)
  + 0.000293 * sin(3.0*Mrad);
  double sunlong = L + Cent;


  double nu = M + Cent;
  double nurad = nu / DEG_IN_RADIAN;

  double R = (1.0000002 * (1 - e*e)) / (1. + e * cos(nurad));
  R = R + 0.00000543 * sin(A)
  + 0.00001575 * sin(B)
  + 0.00001627 * sin(C)
  + 0.00003076 * cos(D)
  + 0.00000927 * sin(H);

  sunlong = sunlong/DEG_IN_RADIAN;

  sun->dist = R;
  x = cos(sunlong);  // geocentric
  y = sin(sunlong);
  z = 0.;
  astro->eclrot(jd, &x, &y, &z);



  //      --- code to include topocentric correction for sun ....

  astro->geocent(lst,geolat,0.,&xgeo,&ygeo,&zgeo);

  double xtop = x - xgeo*EQUAT_RAD/ASTRO_UNIT;
  double ytop = y - ygeo*EQUAT_RAD/ASTRO_UNIT;
  double ztop = z - zgeo*EQUAT_RAD/ASTRO_UNIT;

  double topodist = sqrt(xtop*xtop + ytop*ytop + ztop*ztop);

  double l = xtop / (topodist);
  double m = ytop / (topodist);
  double n = ztop / (topodist);

  sun->topora = astro->atan_circ(l,m) * HRS_IN_RADIAN;
  sun->topodec = asin(n) * DEG_IN_RADIAN;

  sun->ra = astro->atan_circ(x,y) * HRS_IN_RADIAN;
  sun->dec = asin(z) * DEG_IN_RADIAN;

  sun->x = x * R * -1;  // heliocentric
  sun->y = y * R * -1;
  sun->z = z * R * -1;

  delete astro;
}
//------------------------------------------------------------------------------
// Returns jd at which sun is at a given
// altitude, given jdguess as a starting point.
// Uses  low-precision sun, which is plenty good enough.
double Sun::jd_sun_alt( double alt, double jdguess, double lat, double longit)
{
   Astronomy *astro = new Astronomy;
   double del = 0.002;
   double ra,dec,alt2,alt3,az,par;

   lpsun(jdguess,&ra,&dec);
   double ha = astro->lst(jdguess,longit) - ra;
   astro->horizCoord(dec,ha,lat,&alt2,&az,&par);
   jdguess = jdguess + del;
   lpsun(jdguess,&ra,&dec);
   astro->horizCoord(dec,(astro->lst(jdguess,longit) - ra),lat,&alt3,&az,&par);
   double err = alt3 - alt;
   double deriv = (alt3 - alt2) / del;
   short i = 0;
   while((fabs(err) > 0.1) && (i < 10)) {
      jdguess = jdguess - err/deriv;
      lpsun(jdguess,&ra,&dec);
      astro->horizCoord(dec,(astro->lst(jdguess,longit) - ra),lat,&alt3,&az,&par);
      err = alt3 - alt;
      i++;
      if(i == 9) cout << "Sunrise, set, or twilight calculation not converging!" << endl;
   }
   if(i >= 9) jdguess = -1000.;
   double jdout = jdguess;

   delete astro;
   return(jdout);
}
//------------------------------------------------------------------------------
