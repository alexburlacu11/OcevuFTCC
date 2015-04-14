#include "astronomy.h"

//------------------------------------------------------------------------------
// Constructor
Astronomy::Astronomy()
{
}
//------------------------------------------------------------------------------
// Destructor
Astronomy::~Astronomy()
{
}

//------------------------------------------------------------------------------
//  Computes horizontal coordinates, altitude and azimuth,
//   for declination, hour angle and observatory latitude
//   (decimal degr, hr, degr). Also computes parallactic
//   angle (decimal degr)
void Astronomy::horizCoord(double dec,double ha,double lat, double *altitude, double *azimuth, double *parangle)
{

  double d = dec / DEG_IN_RADIAN;
  double h = ha / HRS_IN_RADIAN;
  double l = lat / DEG_IN_RADIAN;
  double cosdec = cos(d);
  double sindec = sin(d);
  double cosha = cos(h);
  double sinha = sin(h);
  double coslat = cos(l);
  double sinlat = sin(l);
  double x = DEG_IN_RADIAN * asin(cosdec*cosha*coslat + sindec*sinlat);
  double y =  sindec*coslat - cosdec*cosha*sinlat; // due north comp.
  double z =  -1.0 * cosdec*sinha; // due east comp.
  *altitude = x;
  *azimuth = atan2(z,y);

// as it turns out, having knowledge of the altitude and azimuth makes the
// spherical trig of the parallactic angle less ambiguous ... so do it here!
// Method uses the "astronomical triangle" connecting celestial pole, object,
// and zenith ... now know all the other sides and angles, so we can crush it.

  if(cosdec != 0.)  // protect divide by zero ...
  {
     double sinp = -1. * sin(*azimuth) * coslat / cosdec;
     // spherical law of sines .. note cosdec = sin of codec,
     //                                coslat = sin of colat ....
     double cosp = -1. * cos(*azimuth) * cosha - sin(*azimuth) * sinha * sinlat;
     // spherical law of cosines ... also transformed to local available variables.
     *parangle = atan2(sinp,cosp) * DEG_IN_RADIAN;
     // let the library function find the quadrant ...
  }
  else { // you're on the pole
     if(lat >= 0.) *parangle = 180.;
     else *parangle = 0.;
  }

  *azimuth *= DEG_IN_RADIAN;  // done with taking trig functions of it ...
  while(*azimuth < 0.) *azimuth += 360.;  // force 0 -> 360
  while(*azimuth >= 360.) *azimuth -= 360.;

}
//------------------------------------------------------------------------------
// Computes the secant of z, assuming the object is not too low to the horizon;
// returns 100. if the object is low but above the horizon, -100. if the object
// is just below the horizon.
double Astronomy::secant_z(double alt)
{
  double secz;
  if(alt != 0)
    secz = 1. / sin(alt / DEG_IN_RADIAN);
  else
    secz = 100.;
  if(secz > 100.) secz = 100.;
  if(secz < -100.) secz = -100.;
  return(secz);
}
//------------------------------------------------------------------------------
// returns the true airmass for a given secant z.
double Astronomy::true_airmass(double secz)
{
  double coef[5];
  coef[1] = 2.879465E-3;
  coef[2] = 3.033104E-3;
  coef[3] = 1.351167E-3;
  coef[4] = -4.716679E-5;
  if(secz < 0.) return(-1.);  // out of range.
  if(secz > 12) return (secz - 1.5);  // shouldn't happen ....
  double seczmin1 = secz - 1.;
  // evaluate polynomial ...
  double result = 0;
  int ord = 4;
  for(int i = ord; i > 0; i--)
    result = (result + coef[i]) * seczmin1;
  // no zeroth order term.
  result = secz - result;
  return(result);
}
//------------------------------------------------------------------------------
// Returns hour angle at which object at dec is at altitude alt.
// If object is never at this altitude, signals with special
// return values 1000 (always higher) and -1000 (always lower).
double Astronomy::ha_alt(double dec,double lat,double alt)
{
  double min_alt;
  double max_alt;
  min_max_alt(lat,dec,&min_alt,&max_alt);
  if(alt < min_alt)
  {
    return(1000.);  // flag value - always higher than asked
  }
  if(alt > max_alt)
  {
    return(-1000.); // flag for object always lower than asked
  }
  double d = PI_OVER_2 - dec / DEG_IN_RADIAN;
  double l = PI_OVER_2 - lat / DEG_IN_RADIAN;
  double coalt = PI_OVER_2 - alt / DEG_IN_RADIAN;
  double x = (cos(coalt) - cos(d)*cos(l)) / (sin(d)*sin(l));
  if(fabs(x) <= 1.)
  {
    return(acos(x) * HRS_IN_RADIAN);
  }
  else
  {
    std::cout << "Error in ha_alt ... acos(>1)." << std::endl;
    return(1000.);
  }
}
//------------------------------------------------------------------------------
// returns radian angle 0 to 2pi for coords x, y -- get that quadrant right !!
double Astronomy::atan_circ( double x, double y)
{
   if((x == 0.) && (y == 0.)) return(0.);
   double theta = atan2(y,x);
   while(theta < 0.) theta += TWOPI;
   return(theta);
}
//------------------------------------------------------------------------------
// Computes minimum and maximum altitude for a given dec and latitude.
void Astronomy::min_max_alt( double lat, double dec, double *min_alt, double *max_alt)
{
  double l = lat / DEG_IN_RADIAN;
  double d = dec / DEG_IN_RADIAN;
  double x = cos(d)*cos(l) + sin(d)*sin(l);
  if(fabs(x) <= 1.)
  {
    *max_alt = asin(x) * DEG_IN_RADIAN;
  }
  else
  {
    std::cout << "Error in min_max_alt -- arcsin(>1)(1)" << std::endl;
  }
  x = sin(d)*sin(l) - cos(d)*cos(l);
  if(fabs(x) <= 1.)
  {
    *min_alt = asin(x) * DEG_IN_RADIAN;
  }
  else
  {
    std::cout << "Error in min_max_alt -- arcsin(>1)(2)" << std::endl;
  }
}
//------------------------------------------------------------------------------
// Angle subtended by two positions in the sky --
// Return value is in radians.  Hybrid algorithm works down
// to zero separation except very near the poles.
// arguments in decimal hrs and decimal degrees
double Astronomy::subtend(double ra1,double dec1,double ra2,double dec2)
{
  double r1 = ra1 / HRS_IN_RADIAN;
  double d1 = dec1 / DEG_IN_RADIAN;
  double r2 = ra2 / HRS_IN_RADIAN;
  double d2 = dec2 / DEG_IN_RADIAN;
  double x1 = cos(r1)*cos(d1);
  double y1 = sin(r1)*cos(d1);
  double z1 = sin(d1);
  double x2 = cos(r2)*cos(d2);
  double y2 = sin(r2)*cos(d2);
  double z2 = sin(d2);
  double theta = acos(x1*x2+y1*y2+z1*z2);
  // use flat Pythagorean approximation if the angle is very small
  // *and* you're not close to the pole; avoids roundoff in arccos.
  if(theta < 1.0e-5)  // seldom the case, so don't combine test
  {
    if(fabs(dec1) < (PI_OVER_2 - 0.001) &&
       fabs(dec2) < (PI_OVER_2 - 0.001))
    {
      // recycled variables here...
      x1 = (ra2 - ra1) * cos((dec1+dec2)/2.);
      x2 = dec2 - dec1;
      theta = sqrt(x1*x1 + x2*x2);
    }
  }
  return(theta);
}
//------------------------------------------------------------------------------
// returns the local MEAN sidereal time (dec hrs) at julian date jd at west
// longitude long (decimal hours).  Follows definitions in 1992 Astronomical
// Almanac, pp. B7 and L2. Expression for GMST at 0h ut referenced to Aoki et al,
// A&A 105, p.359, 1982.  On workstations, accuracy (numerical only!) is about
// a millisecond in the 1990s.
double Astronomy::lst(double jd,double longitude)
{
  double sid_g;
  double jdmid;
  double ut;
  double jdfrac = jd - floor(jd);
  if(jdfrac < 0.5)
  {
    jdmid = floor(jd) - 0.5;
    ut = jd - floor(jd) + 0.5;
  } else {
    jdmid = floor(jd) + 0.5;
    ut = jd - floor(jd) - 0.5;
  }
  double t = (jdmid - J2000)/36525.0;
  sid_g = (24110.54841+8640184.812866*t+0.093104*t*t-6.2e-6*t*t*t)/SEC_IN_DAY;
  sid_g = sid_g - floor(sid_g);
  sid_g = sid_g + 1.0027379093 * ut - longitude/24.;
  sid_g = (sid_g - floor(sid_g)) * 24.;
  if(sid_g < 0.) sid_g = sid_g + 24.;
  return(sid_g);
}
//------------------------------------------------------------------------------
// Converts a "babylonian" (sexigesimal) structure into
// double-precision floating point ("decimal") number.
double Astronomy::bab_to_dec( coord bab)
{
   double x = bab.sign * (bab.hh + bab.mm / 60. + bab.ss / 3600.);
   return(x);
}
//------------------------------------------------------------------------------
// Function for converting decimal to babylonian hh mm ss.ss
Astronomy::coord Astronomy::dec_to_bab ( double deci)
{
   coord bab;
   if (deci >= 0.)
   {
       bab.sign = 1;
   } else {
      bab.sign = -1;
      deci = -1. * deci;
   }
   bab.hh = floor(deci);
   bab.mm = floor(60. * (deci - bab.hh));
   bab.ss = 3600. * (deci - bab.hh - bab.mm / 60.);
   return bab;
}
// ---------------------------------------------------------------------------------
// Build a string with coordinate or time in sexigesimal units.
// Add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
// Any other value to add nothing.
string Astronomy::print_time( coord tme, int UT, int secPrec)
{
  std::ostringstream oss;
  string str;

  std::ostringstream hss;
  string h;
  if( tme.sign==-1 )
  {
    if( tme.hh<10)
      hss << " -" << tme.hh ;
    else
      hss << "-" << tme.hh ;
  }
  else
  {
    if( tme.hh<10 )
      hss << "  " << tme.hh ;
    else
      hss << " " << tme.hh ;
  }
  h=hss.str();

  ostringstream mss;
  string m;
  if( tme.mm<10 )
    mss << "0" << tme.mm ;
  else
    mss  << tme.mm ;
  m=mss.str();

  oss << " " << h << ":"  << m << ":" << fixed << setprecision (secPrec) << tme.ss;
  str=oss.str();
//  add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
  if( UT == 0)
  {
    str = str +" local time";
  } else if( UT == 1) {
    str = str + " UT";
  }
  return str;
}
// ---------------------------------------------------------------------------------
// Build a string with coordinate or time in sexigesimal units.
// input time/coordinate is given in decimal unit.
// Add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
// Any other value to add nothing.
string Astronomy::print_time( double t, int UT, int secPrec)
{
  coord tme = dec_to_bab(t);
  string str = print_time( tme, UT, secPrec);
  return str;
}
// ---------------------------------------------------------------------------------
// Adjusts a time (decimal hours) to be between -12 and 12,
// generally used for hour angles.
double Astronomy::adj_time( double x)
{
   if(fabs(x) < 100000.)     // too inefficient for this!
   {
      while(x > 12.) x = x - 24.;
      while(x < -12.)  x = x + 24.;
   }
   else
   {
      cout << "Out of bounds in adj_time!" << endl;
   }
   return(x);
}
//------------------------------------------------------------------------------
// Rotates ecliptic rectangular coords x, y, z to equatorial (all assumed of date)
void Astronomy::eclrot( double jd,  double *x,  double *y,  double *z)
{
   double T = (jd - J2000) / 36525.0;  // centuries since J2000
   double incl = (23.439291 + T * (-0.0130042 - 0.00000016 * T))/DEG_IN_RADIAN;
   // 1992 Astron Almanac, p. B18, dropping the cubic term, which is 2 milli-arcsec!
   double xpr = *x; // x remains the same.
   double ypr = cos(incl) * *y - sin(incl) * *z;
   double zpr = sin(incl) * *y + cos(incl) * *z;
   *x = xpr;
   *y = ypr;
   *z = zpr;
}
//------------------------------------------------------------------------------
// Assuming x is an angle in degrees, returns modulo 360 degrees.
double Astronomy::circulo( double x)
{
   int n = (int)(x / 360.);
   return(x - 360. * n);
}
//------------------------------------------------------------------------------
// Computes the geocentric coordinates from the geodetic
// (standard map-type) longitude, latitude, and height.
// These are assumed to be in decimal hours, decimal degrees, and
// meters respectively. Notation generally follows 1992 Astr Almanac, p. K11.
void Astronomy::geocent( double geolong, double geolat, double height, double *x_geo, double *y_geo, double *z_geo)
{
   double glt = geolat / DEG_IN_RADIAN;
   double glg = geolong / HRS_IN_RADIAN;
   double denom = (1. - FLATTEN) * sin(glt);
   denom = cos(glt) * cos(glt) + denom*denom;
   double C_geo = 1. / sqrt(denom);
   double S_geo = (1. - FLATTEN) * (1. - FLATTEN) * C_geo;
   C_geo = C_geo + height / EQUAT_RAD; // deviation from almanac notation -- include height here.
   S_geo = S_geo + height / EQUAT_RAD;
   *x_geo = C_geo * cos(glt) * cos(glg);
   *y_geo = C_geo * cos(glt) * sin(glg);
   *z_geo = S_geo * sin(glt);
}
//------------------------------------------------------------------------------
// Given a julian date in 1900-2100, returns the correction delta t which is:
//      TDT - UT (after 1983 and before 1998)
//      ET - UT (before 1983)
//      an extrapolated guess  (after 2001).
//
// For dates in the past (<= 2001 and after 1900) the value is linearly
// interpolated on 5-year intervals; for dates after the present, an
// extrapolation is used, because the true value of delta t cannot be
// predicted precisely.  Note that TDT is essentially the modern version of
// ephemeris time with a slightly cleaner definition.
//
// Where the algorithm shifts there will be a small (< 0.1 sec) discontinuity.
// Also, the 5-year linear interpolation scheme can lead to errors as large as
// 0.5 seconds in some cases, though usually rather smaller.   One seldom has
// actual UT to work with anyway, since the commonly-used UTC is tied to TAI
// within an integer number of seconds.
double Astronomy::etcorr( double jd)
{
   double jd1900 = 2415019.5;
   double dates[31];
   double delts[31];
   double year, delt;
   int i;

   for(int i = 0; i <= 20; i++) dates[i] = 1900 + (double) i * 5.;
   for(int i = 21; i <= 30; i++) dates[i] = 1900 + (double) i ;

   delts[0]  = -2.72;  delts[1]  =  3.86; delts[2]  = 10.46;
   delts[3]  = 17.20;  delts[4]  = 21.16; delts[5]  = 23.62;
   delts[6]  = 24.02;  delts[7]  = 23.93; delts[8]  = 24.33;
   delts[9]  = 26.77;  delts[10] = 29.15; delts[11] = 31.07;
   delts[12] = 33.15;  delts[13] = 35.73; delts[14] = 40.18;
   delts[15] = 45.48;  delts[16] = 50.54; delts[17] = 54.34;
   delts[18] = 56.86;  delts[19] = 60.78; delts[20] = 63.83;
   delts[21] = 64.09;  delts[22] = 64.30; delts[23] = 64.47;
   delts[24] = 64.57;  delts[25] = 64.69;
// 2005:  the last accurately tabulated one in the 2007 Almanac
   delts[26] = 64.9;  // 2006: extrapolated in the 2007 Almanac
   delts[27] = 65.;   // 2007: extrapolated in the 2007 Almanac
   delts[28] = 65.;   // 2008: extrapolated in the 2007 Almanac
   delts[29] = 66.;   // 2009: extrapolated in the 2007 Almanac
   delts[30] = 66.;   // 2010: extrapolated in the 2007 Almanac


   year = 1900. + (jd - jd1900) / 365.25;
   delt = 0.;

   if(year < 2001. && year >= 1900.)
   {
      i = (year - 1900) / 5;
      delt = delts[i] +
       ((delts[i+1] - delts[i])/(dates[i+1] - dates[i])) * (year - dates[i]);
   }
   else if (year >= 2001. && year <= 2010.)
   {
      i = year - 1900;
      delt = delts[i];
   }
   else if (year > 2010. && year < 2100.)
   {
      // rough extrapolation from 2001 Almanac value
      delt = 31.69 + (2.164e-3) * (jd - 2436935.4);
   }
   else if (year < 1900)
   {
      printf("etcorr ... no ephemeris time data for < 1900.\n");
      delt = 0.;
   }
   else if (year >= 2100.)
   {
      printf("etcorr .. very long extrapolation in delta T - inaccurate.\n");
      delt = 180.; // who knows?
   }

   return(delt);
}
//------------------------------------------------------------------------------
// evaluates a polynomial expansion for the approximate brightening
//   in magnitudes of the zenith in twilight compared to its
//   value at full night, as function of altitude of the sun (in degrees).
//   To get this expression the author looked in Meinel, A.,
//   & Meinel, M., "Sunsets, Twilight, & Evening Skies", Cambridge U.
//   Press, 1983; there's a graph on p. 38 showing the decline of
//   zenith twilight. The author read points off this graph and fit them with a
//   polynomial; the author don't even know what band there data are for!
// Comparison with Ashburn, E. V. 1952, JGR, v.57, p.85 shows that this
//   is a good fit to his B-band measurements.
float Astronomy::ztwilight( double alt)
{
   float y = (-1.* alt - 9.0) / 9.0;
   float val = ((2.0635175 * y + 1.246602) * y - 9.4084495)*y + 6.132725;
   return(val);
}
//------------------------------------------------------------------------------
// Converts cartesian coordinate (x,y,z) to right ascension and declination,
// returned in decimal hours and decimal degrees.
void Astronomy::xyz_cel( double x, double y, double z, double *ra, double *dec)
{
   // normalize explicitly and check for bad input
   double mod = sqrt(x*x + y*y + z*z);
   if(mod > 0.)
   {
      x = x / mod;
      y = y / mod;
      z = z / mod;
   } else {   // this has never happened
     cout << "Bad data in xyz_cel .... zero modulus position vector." << endl;
     *ra = 0.;
     *dec = 0.;
     return;
   }

   double xy = sqrt(x*x + y*y);
   if(xy < 1.0e-11) {   // practically on a pole -- limit is arbitrary ...
      *ra = 0.;  // degenerate anyway
      *dec = PI_OVER_2;
      if(z < 0.) *dec *= -1.;
   } else {      // in a normal part of the sky ...
      *dec = asin(z);
      *ra = atan_circ(x,y);
   }

   *ra *= HRS_IN_RADIAN;
   *dec *= DEG_IN_RADIAN;
}
//------------------------------------------------------------------------------
// Corrects celestial unit vector for aberration due to earth's motion.
// Uses accurate sun position ... replace with crude one for more speed if needed.
//  epoch, decimal year ...
//  vec[];   celestial unit vector ...
//  from_std;  1 = apply aberration, -1 = take aberration out.
void Astronomy::aberrate( double epoch, double vec[3], int from_std)
{
   Sun *sun1 = new Sun;
   Sun *sun2 = new Sun;

   // find heliocentric velocity of earth as a fraction of the speed of light ...

   double jd = J2000 + (epoch - 2000.) * 365.25;
   double jd1 = jd - EARTH_DIFF;
   double jd2 = jd + EARTH_DIFF;

   sun1->accusun(jd1,0.,0.,sun1);
   sun2->accusun(jd2,0.,0.,sun2);

   double Xdot = KMS_AUDAY*(sun2->x - sun1->x)/(2.*EARTH_DIFF * SPEED_OF_LIGHT);  // numerical differentiation
   double Ydot = KMS_AUDAY*(sun2->y - sun1->y)/(2.*EARTH_DIFF * SPEED_OF_LIGHT);  // crude but accurate
   double Zdot = KMS_AUDAY*(sun2->z - sun1->z)/(2.*EARTH_DIFF * SPEED_OF_LIGHT);

   // approximate correction ... non-relativistic but very close.

   vec[1] += from_std * Xdot;
   vec[2] += from_std * Ydot;
   vec[3] += from_std * Zdot;

   double norm = pow((vec[1] * vec[1] + vec[2] * vec[2] + vec[3] * vec[3]), 0.5);

   vec[1] = vec[1] / norm;
   vec[2] = vec[2] / norm;
   vec[3] = vec[3] / norm;

   delete sun1;
   delete sun2;

}
//------------------------------------------------------------------------------
// Computes the nutation parameters delta psi and delta epsilon
// at julian epoch (in years) using approximate formulae given by Jean Meeus,
// Astronomical Formulae for Calculators, Willman-Bell, 1985, pp. 69-70.
// Accuracy appears to be a few hundredths of an arcsec or better and numerics
// have been checked against his example. Nutation parameters are returned in
// radians.
void Astronomy::nutation_params( double date_epoch,  double *del_psi,  double *del_ep)
{
   double jd = (date_epoch - 2000.) * 365.25 + J2000;
   double T = (jd - 2415020.0) / 36525.;

   double L = 279.6967 + (36000.7689  + 0.000303 * T) * T;
   double Lprime = 270.4342 + (481267.8831 - 0.001133 * T ) * T;
   double M = 358.4758 + (35999.0498 - 0.000150 * T) * T;
   double Mprime = 296.1046 + (477198.8491 + 0.009192 * T ) * T;
   double Omega = 259.1833 - (1934.1420 - 0.002078 * T) * T;

   L = L / DEG_IN_RADIAN;
   Lprime = Lprime / DEG_IN_RADIAN;
   M = M / DEG_IN_RADIAN;
   Mprime = Mprime / DEG_IN_RADIAN;
   Omega = Omega / DEG_IN_RADIAN;

   *del_psi = -1. * (17.2327 + 0.01737 * T) * sin(Omega)
      - (1.2729 + 0.00013 * T) * sin(2. * L)
      + 0.2088 * sin(2 * Omega)
      - 0.2037 * sin(2 * Lprime)
      + (0.1261 - 0.00031 * T) * sin(M)
      + 0.0675 * sin(Mprime)
      - (0.0497 - 0.00012 * T) * sin(2 * L + M)
      - 0.0342 * sin(2 * Lprime - Omega)
      - 0.0261 * sin(2 * Lprime + Mprime)
      + 0.0214 * sin(2 * L - M)
      - 0.0149 * sin(2 * L - 2 * Lprime + Mprime)
      + 0.0124 * sin(2 * L - Omega)
      + 0.0114 * sin(2 * Lprime - Mprime);
   *del_ep = (9.2100 + 0.00091 * T) * cos(Omega)
      + (0.5522 - 0.00029 * T) * cos(2 * L)
      - 0.0904 * cos(2 * Omega)
      + 0.0884 * cos(2. * Lprime)
      + 0.0216 * cos(2 * L + M)
      + 0.0183 * cos(2 * Lprime - Omega)
      + 0.0113 * cos(2 * Lprime + Mprime)
      - 0.0093 * cos(2 * L - M)
      - 0.0066 * cos(2 * L - Omega);
   *del_psi = *del_psi / ARCSEC_IN_RADIAN;
   *del_ep  = *del_ep  / ARCSEC_IN_RADIAN;
}
//------------------------------------------------------------------------------
// General routine for precession and apparent place.
// Either transforms from current epoch (given by jd) to a standard epoch or
// back again, depending on value of the switch "from_std":
//      1 transforms from standard to current,
//     -1 goes the other way.
// Optionally does apparent place including nutation and annual aberration
// (but neglecting diurnal aberration,parallax, proper motion, and GR deflection
// of light); switch for this is "just_precess",
//     1 does only precession,
//     0 includes other aberration & nutation.
// Precession uses a matrix procedures as outlined in Taff's Computational
// Spherical Astronomy book. This is the so-called 'rigorous' method which
// should give very accurate answers all over the sky over an interval of
// several centuries. Naked eye accuracy holds to ancient times, too. Precession
// constants used are the new IAU1976 -- the 'J2000' system. Nutation is
// incorporated into matrix formalism by constructing an approximate nutation
// matrix and taking a matrix product with precession matrix. Aberration is done
// by adding the vector velocity of the earth to the velocity of the light ray,
// not kosher relativistically, but empirically correct to a high order for the
// angle.
// rin, din;   input ra and dec
// rout, dout;   output
void Astronomy::precess( double rin, double din, double std_epoch, double date_epoch,
              double *rout, double *dout, int just_precess, int from_std)
{
   double p[4][4];      // elements of the rotation matrix
   double n[4][4];      // elements of the nutation matrix
   double r[4][4];      // their product
   double t[4][4];      // temporary matrix for inversion
   double del_psi, del_eps;  // nutation angles in radians
   double orig[4];      // original unit vector
   double fin[4];       // final unit vector

   double ti = (std_epoch - 2000.) / 100.;
   double tf = (date_epoch  - 2000. - 100. * ti) / 100.;

   double zeta = (2306.2181 + 1.39656 * ti + 0.000139 * ti * ti) * tf +
    (0.30188 - 0.000344 * ti) * tf * tf + 0.017998 * tf * tf * tf;
   double z = zeta + (0.79280 + 0.000410 * ti) * tf * tf + 0.000205 * tf * tf * tf;
   double theta = (2004.3109 - 0.8533 * ti - 0.000217 * ti * ti) * tf
     - (0.42665 + 0.000217 * ti) * tf * tf - 0.041833 * tf * tf * tf;

   // convert to radians
   zeta = zeta / ARCSEC_IN_RADIAN;
   z = z / ARCSEC_IN_RADIAN;
   theta = theta / ARCSEC_IN_RADIAN;

   // compute the necessary trig functions for speed and simplicity
   double cosz = cos(z);
   double coszeta = cos(zeta);
   double costheta = cos(theta);
   double sinz = sin(z);
   double sinzeta = sin(zeta);
   double sintheta = sin(theta);

   // compute the elements of the precession matrix -- set up
   //   here as *from* standard epoch *to* input jd.
   p[1][1] = coszeta * cosz * costheta - sinzeta * sinz;
   p[1][2] = -1. * sinzeta * cosz * costheta - coszeta * sinz;
   p[1][3] = -1. * cosz * sintheta;

   p[2][1] = coszeta * sinz * costheta + sinzeta * cosz;
   p[2][2] = -1. * sinzeta * sinz * costheta + coszeta * cosz;
   p[2][3] = -1. * sinz * sintheta;

   p[3][1] = coszeta * sintheta;
   p[3][2] = -1. * sinzeta * sintheta;
   p[3][3] = costheta;

   if(just_precess == XFORM_DOAPPAR)   // if apparent place called for
   {
      // do the same for the nutation matrix.
      nutation_params(date_epoch, &del_psi, &del_eps);
      double eps = 0.409105;  // rough obliquity of ecliptic in radians

      n[1][1] = 1.;
      n[2][2] = 1.;
      n[3][3] = 1.;
      n[1][2] = -1. * del_psi * cos(eps);
      n[1][3] = -1. * del_psi * sin(eps);
      n[2][1] = -1. * n[1][2];
      n[2][3] = -1. * del_eps;
      n[3][1] = -1. * n[1][3];
      n[3][2] = -1. * n[2][3];

      // form product of precession and nutation matrices
      for(int i = 1; i <= 3; i++)
      {
         for(int j = 1; j <= 3; j++)
         {
            r[i][j] = 0.;
            for(int k = 1; k <= 3; k++)
               r[i][j] += p[i][k] * n[k][j];
         }
      }
   } else {          // if you're just precessing
      for(int i = 1; i <= 3; i++)
      {
         for(int j = 1; j <=3; j++)
            r[i][j] = p[i][j];  // simply copy precession matrix
      }
   }

   // The inverse of a rotation matrix is its transpose
   if(from_std == XFORM_TOSTDEP)
   {
       // if you're transforming back to std epoch, rather than forward from std
      for(int i = 1; i <= 3; i++)
      {
         for(int j = 1; j <= 3; j++)
            t[i][j] = r[j][i];        // store transpose
      }
      for(int i = 1; i <= 3; i++)
      {
         for(int j = 1; j <= 3; j++)
            r[i][j] = t[i][j];        // replace original w/ transpose
      }
   }

   // finally, transform original coordinates
   double radian_ra = rin / HRS_IN_RADIAN;
   double radian_dec = din / DEG_IN_RADIAN;

   orig[1] = cos(radian_dec) * cos(radian_ra);
   orig[2] = cos(radian_dec) * sin(radian_ra);
   orig[3] = sin(radian_dec);

   if(from_std == XFORM_TOSTDEP && just_precess == XFORM_DOAPPAR)
      // if you're transforming from jd to std epoch, and doing apparent place,
      // first step is to de-aberrate while still in epoch of date
      aberrate(date_epoch, orig, from_std);


   for(int i = 1; i<=3; i++)
   {
      fin[i] = 0.;
      for(int j = 1; j<=3; j++)
      {
         fin[i] += r[i][j] * orig[j];
      }
   }

   if(from_std == XFORM_FROMSTD && just_precess == XFORM_DOAPPAR)
      // if you're transforming from std epoch to jd,
      // last step is to apply aberration correction once you're in
      // equinox of that jd.
      aberrate(date_epoch, fin, from_std);

   // convert back to spherical polar coords
   xyz_cel(fin[1], fin[2], fin[3], rout, dout);

   return;
}
//------------------------------------------------------------------------------
//Computes near horizon refraction
// formula for near horizon, function-ized for iteration ...
// Almanac 1992, p. B62 -- ignores temperature variation
double Astronomy::near_hor_refr( double app_alt, double pressure)
{
   double r = pressure *
      (0.1594 + 0.0196 * app_alt + 0.00002 * app_alt * app_alt) /
      (293. * (1. + 0.505 * app_alt + 0.0845 * app_alt * app_alt));
   return(r);
}
//------------------------------------------------------------------------------
// Computes refraction size for a given altitude
// Almanac for 1992, p. B 62.  Ignores variation in temperature and just assumes
// T = 20 celsius.
//   alt;    altitude in degrees
//   elev;   elevation in meters
double Astronomy::refract_size( double alt, double  elev)
{
   double  r;
   double altrad = alt / DEG_IN_RADIAN;

   double pressure = 1013. * exp(-1. * elev/8620.);
   // exponential atmosphere at T = 20 C, g = 980 cm/s^2,
   // and mean molecular wgt 28.8

   if(alt > 89.9) // avoid blowing up
      return(0.);
   else if (alt >= 15.0)
   {
      r = 0.00452 * pressure / (293. * tan(altrad));
      return(r);
   } else {  // here have to start worrying about distinction between
             // apparent and true altitude ... a pity as true altitude is
             // what is handed in ...
      double crit_alt = -1. * pressure * 0.1594 / 293.;
      // that's the *true* altitude corresponding to an *apparent*
      // altitude of zero ... forget it if it's below this.
      if (alt > crit_alt)       // go ahead and get it ...
      {
         double app_alt = alt;  // initial ...
         for(int i = 1; i <= 3; i++)
         {
           // tests show 3 iterations is good to < 0.5 arcmin for objects below
           // geom horizon just barely rising .. further accuracy is spurious.
           r = near_hor_refr(app_alt, pressure);
           app_alt = alt + r;
         }
         r = near_hor_refr(app_alt, pressure);
         return(r);
      } else {
         return(-1.);          // below horizon.
      }
   }
}
//------------------------------------------------------------------------------
// Corrects local equatorial coordinates for refraction
// if sense == 1 , applies refraction to a true ha and dec;
// if sense == -1, de-corrects already refracted coordinates.
// Uses elevation of observatory above sea level to estimate a mean atmospheric
// pressure.
// The calculation is done by computing xyz coordinates in the horizon system,
// adding to the vertical component, renormalizing back to a unit vector,
// rotating to the polar system, and transforming back to ha and dec .... a long
// way around the barn, but completely general.
void Astronomy::refract_corr( double *ha, double *dec, double latitude, double *size, int sense)
{
   double localdec = *dec / DEG_IN_RADIAN;
   double localha = *ha / HRS_IN_RADIAN;
   double lat = latitude / DEG_IN_RADIAN;
   double sinlat = sin(lat);
   double coslat = cos(lat);

   double x =  cos(localdec)*cos(localha)*coslat + sin(localdec)*sinlat;      // vertical component
   double y =  sin(localdec)*coslat - cos(localdec)*cos(localha)*sinlat;      // due N comp.
   double z =  -1. * cos(localdec)*sin(localha);      // due east comp.

   *size = refract_size(DEG_IN_RADIAN * asin(x), 0.);       // this gives zero for zenith

   if(*size > 0.)  // guard against singular result at zenith
   {
      double norm = pow((y * y + z * z), 0.5);  // in-ground component

      x = norm * tan(atan(x/norm) + sense * *size / DEG_IN_RADIAN);
      norm = pow((x*x + y*y + z*z),0.5);

      x = x / norm; y = y / norm; z = z / norm;

      double xpr = x * coslat - y * sinlat;
      double ypr = x * sinlat + y * coslat;

      *dec = asin(ypr) * DEG_IN_RADIAN;
      *ha = -1. * atan2(z, xpr) * HRS_IN_RADIAN;
   }
}
//------------------------------------------------------------------------------
// Algorithm for 3-d Euler rotation into galactic.
// Perfectly rigorous, and with reasonably accurate input numbers derived from
// original IAU definition of galactic pole (12 49, +27.4, 1950) and zero of
// long (at PA 123 deg from pole.)
void Astronomy::galact( double ra, double dec, double epoch, double *glong, double *glat)
{
   double  p11= -0.066988739415,
      p12= -0.872755765853,
      p13= -0.483538914631,
      p21=  0.492728466047,
      p22= -0.450346958025,
      p23=  0.744584633299,
      p31= -0.867600811168,
      p32= -0.188374601707,
      p33=  0.460199784759;  // derived from Euler angles of
        // theta   265.610844031 deg (rotates x axis to RA of galact center),
        // phi     28.9167903483 deg (rotates x axis to point at galact cent),
        // omega   58.2813466094 deg (rotates z axis to point at galact pole)

   double r1950,d1950;

/*   EXCISED CODE .... creates matrix from Euler angles. Resurrect if
     necessary to create new Euler angles for better precision.
     Program evolved by running and calculating angles,then initializing
     them to the values they will always have, thus saving space and time.

   cosphi = cos(phi); and so on
   p11 = cosphi * costhet;
   p12 = cosphi * sinthet;
   p13 = -1. * sinphi;
   p21 = sinom*sinphi*costhet - sinthet*cosom;
   p22 = cosom*costhet + sinthet*sinphi*sinom;
   p23 = sinom*cosphi;
   p31 = sinom*sinthet + cosom*sinphi*costhet;
   p32 = cosom*sinphi*sinthet - costhet*sinom;
   p33 = cosom * cosphi;

   printf("%15.10f %15.10f %15.10f\n",p11,p12,p13);
   printf("%15.10f %15.10f %15.10f\n",p21,p22,p23);
   printf("%15.10f %15.10f %15.10f\n",p31,p32,p33);

   double check = p11*(p22*p33-p32*p23) - p12*(p21*p33-p31*p23) +
      p13*(p21*p32-p22*p31);
   printf("Check: %lf\n",check);  check determinant .. ok

    END OF EXCISED CODE..... */

   // precess to 1950
   precess(ra,dec,1950.,epoch,&r1950,&d1950,
      XFORM_JUSTPRE,XFORM_TOSTDEP);   // transform *to* std epoch
   r1950 = r1950 / HRS_IN_RADIAN;
   d1950 = d1950 / DEG_IN_RADIAN;

   // form direction cosines
   double x0 = cos(r1950) * cos(d1950);
   double y0 = sin(r1950) * cos(d1950);
   double z0 = sin(d1950);

   // rotate them
   double x1 = p11*x0 + p12*y0 + p13*z0;
   double y1 = p21*x0 + p22*y0 + p23*z0;
   double z1 = p31*x0 + p32*y0 + p33*z0;

   // translate to spherical polars for Galactic coords.
   *glong = atan_circ(x1,y1)*DEG_IN_RADIAN;
   *glat = asin(z1)*DEG_IN_RADIAN;
}
//------------------------------------------------------------------------------
// converts ra and dec to ecliptic coords -- precesses to current
//   epoch first (and hands current epoch back for printing.)
//  ra in decimal hrs, other coords in dec. deg.
void Astronomy::eclipt( double ra, double dec, double epoch, double jd,
             double *curep, double *eclong, double *eclat)
{
   double racur, decur;

   double T = (jd - J2000)/36525.;  // centuries since J2000
   *curep = 2000. + (jd - J2000) / 365.25;

   double incl = (23.439291 + T * (-0.0130042 - 0.00000016 * T))/DEG_IN_RADIAN;
   // 1992 Astron Almanac, p. B18, dropping the cubic term, which is 2 milli-arcsec!

   precess(ra,dec,epoch,*curep,&racur,&decur,
      XFORM_JUSTPRE,XFORM_FROMSTD);
   racur = racur / HRS_IN_RADIAN;
   decur = decur / DEG_IN_RADIAN;

   double x0=cos(decur)*cos(racur);
   double y0=cos(decur)*sin(racur);
   double z0=sin(decur);

   double x1=x0;  // doesn't change
   double y1 = cos(incl)*y0 + sin(incl)*z0;
   double z1 = -1 * sin(incl)*y0 + cos(incl)*z0;
   *eclong = atan_circ(x1,y1) * DEG_IN_RADIAN;
   *eclat = asin(z1) * DEG_IN_RADIAN;
}
//------------------------------------------------------------------------------
// Corrects heliocentric position and velocity to the solar system barycenter.
// This routine takes the position x,y,z and velocity xdot,ydot,zdot, assumed
// heliocentric, and corrects them to the solar system barycenter taking into
// account the nine major planets.  Routine evolved by inserting planetary data
// (given above) into an earlier, very crude barycentric correction.
void Astronomy::barycor( double jd, double *x, double *y, double *z,
              double *xdot, double *ydot, double *zdot)
{
   Planets *plnt = new Planets;
   double xp, yp, zp, xvp, yvp, zvp;
   double xc=0.,yc=0.,zc=0.,xvc=0.,yvc=0.,zvc=0.;

   plnt->comp_el(jd);

   for(int p=1;p<=9;p++)    // sum contributions of the planets
   {
      plnt->planetxyz(p,jd,&xp,&yp,&zp);
      xc = xc + plnt->el[p].mass * xp;  // mass is fraction of solar mass
      yc = yc + plnt->el[p].mass * yp;
      zc = zc + plnt->el[p].mass * zc;
      plnt->planetvel(p,jd,&xvp,&yvp,&zvp);
      xvc = xvc + plnt->el[p].mass * xvp;
      yvc = yvc + plnt->el[p].mass * yvp;
      zvc = zvc + plnt->el[p].mass * zvc;
   }
   // normalize properly and rotate corrections to equatorial coords
   xc = xc / SS_MASS;
   yc = yc / SS_MASS;
   zc = zc / SS_MASS;     // might as well do it right ...

   eclrot(jd, &xc, &yc, &zc);

   xvc = xvc * KMS_AUDAY / SS_MASS;
   yvc = yvc * KMS_AUDAY / SS_MASS;
   zvc = zvc * KMS_AUDAY / SS_MASS;
   eclrot(jd, &xvc, &yvc, &zvc);

   // add them in
   *x = *x - xc;  // these are in AU
   *y = *y - yc;
   *z = *z - zc;
   *xdot = *xdot - xvc;
   *ydot = *ydot - yvc;
   *zdot = *zdot - zvc;

   delete plnt;
}
//------------------------------------------------------------------------------
// Computes heliocentric correction for time and velocity
//  Finds heliocentric correction for given jd, ra, dec, ha, and lat.
//  tcor is time correction in seconds, vcor velocity in km/s, to be added to
//  the observed values. Input ra and dec assumed to be at current epoch.
void Astronomy::helcor( double jd, double RA, double DEC, double HA, double lat, double elevsea, double *tcor, double *vcor)
{
  Sun *sun1 = new Sun;
  Sun *sun2 = new Sun;

  double x, y, z;
  double xdot, ydot, zdot;
  double x_geo, y_geo, z_geo;  // geocentric coords of observatory
  double a=499.0047837;  // light travel time for 1 AU, sec

  double dec= DEC/DEG_IN_RADIAN;
  double ra =  RA/HRS_IN_RADIAN;
  double ha =  HA/HRS_IN_RADIAN;

  double xobj = cos(ra) * cos(dec);
  double yobj = sin(ra) * cos(dec);
  double zobj = sin(dec);

  double jd1 = jd - EARTH_DIFF;
  double jd2 = jd + EARTH_DIFF;

  sun1->accusun(jd1,0.,0.,sun1);
  sun2->accusun(jd2,0.,0.,sun2);

  xdot = KMS_AUDAY*(sun2->x - sun1->x)/(2.*EARTH_DIFF);  // numerical differentiation
  ydot = KMS_AUDAY*(sun2->y - sun1->y)/(2.*EARTH_DIFF);  // crude but accurate
  zdot = KMS_AUDAY*(sun2->z - sun1->z)/(2.*EARTH_DIFF);
  barycor(jd,&x,&y,&z,&xdot,&ydot,&zdot);

// heliocentric correction for time:
   *tcor = a * (x*xobj + y*yobj + z*zobj);

// heliocentric correction for velocity:
   *vcor = xdot * xobj + ydot * yobj + zdot * zobj;
// correct diurnal rotation for elliptical earth including obs. elevation
   geocent(0., lat, elevsea, &x_geo, &y_geo, &z_geo);
// longitude set to zero arbitrarily so that x_geo = perp. distance to axis
   *vcor = *vcor - 0.4651011 * x_geo * sin(ha) * cos(dec);
// 0.4651011 = 6378.137 km radius * 2 pi / (86164.1 sec per sidereal day)
// could add time-of-flight across earth's radius here -- but rest of
//   theory is not good to 0.02 seconds anyway.

   delete sun1;
   delete sun2;
}
//------------------------------------------------------------------------------
// Computes the correction from bary/helio centric to local standard of rest
// i.e. (v wrt lsr) = (v helio) + vcor.
// velocity of the sun is taken to be 13 km/s toward 1900 coords 18 0 0 +30 0 0
void Astronomy::lsrcor( double ra, double dec, double epoch, double *vcor)
{
   double ra1900, dec1900;
//   double xdotsun = 0.;
   double ydotsun = -11.258, zdotsun = 6.5;

   precess(ra,dec,1900.,epoch,&ra1900,&dec1900,
      XFORM_JUSTPRE,XFORM_TOSTDEP);   // transform *to* 1900
   //  double x = cos(dec1900/DEG_IN_RADIAN) * cos(ra1900/HRS_IN_RADIAN);
   // ... no x-component in std solar motion
   double y = cos(dec1900/DEG_IN_RADIAN) * sin(ra1900/HRS_IN_RADIAN);
   double z = sin(dec1900/DEG_IN_RADIAN);
   *vcor = y * ydotsun + z * zdotsun;
}
