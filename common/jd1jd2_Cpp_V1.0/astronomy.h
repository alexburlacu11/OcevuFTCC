/** \mainpage
 *
 *<BR>
 * <H1>C++ Classes for astronomical calculations</H1><BR>
 * A C++ library<BR>
 * by Jean-Francois Le Borgne, Astronomer at <I>IRAP</I>, <I>Observatoire Midi-Pyrénées</I>, Toulouse, F EU<BR>
 * Adapted from c program skycalc by  John Thorstensen, Dartmouth College, Hanover, NH USA. Version 6.1, 2005
 * which uses Jean Meeus' algorithms (<B>Astronomical Formulae For Calculators, pub. Willman-Bell.</B>, 1985)<BR>
 * http://www.dartmouth.edu/~physics/people/faculty/thorstensen.html<BR>
 *
 *
 * \section intro_sec Introduction
 * Most comments in code and documentation are from John Thorstensen's code.
 *
 *
 * \section install_sec Installation
 *
 * g++ -o astro observatory.cpp amzer.cpp astronomy.cpp sun.cpp moon.cpp planets.cpp main.cpp
 *
 * \section Usage
 *
 *  ./astro [-h] [-f filename]<BR>
 *  ./astro [-h] [-o name] [-d date] || [-j JD] [-c ra dec equinoxe -m]<BR>
 *    -h : help<BR>
 *    -v : verbose<BR>
 *    -f filename : parameter file<BR>
 *    -o  name : observatory name<BR>
 *    -d  date : calendar date (ex. 2014 6 25 19 35 45.6)<BR>
 *    -j  JD : julian date (ex. 2456834.3165)<BR>
 *    -c  ra dec equinoxe : equatorial coordiantes of object<BR>
 *    -m  minimum height of object above horizon (>0)<BR>
 *    -l  limit acceptable distance to the Moon (degrees)<BR>
 *  <BR>
 *  Examples: ./astro -o \"La Silla\"<BR>
 *            ./astro -o Toulouse<BR>
 *            ./astro -f parameters.txt<BR>
 *  <BR>
 *  (-o -d -j -c) and -f options are incompatible. if both are used, -f superseed -o<BR>
 *  -d and -j are are 2 options for the same parameter, the date. if both are used, -j superseed -d<BR>
 *
 * \section how_to
 * How to use this document
 *
 */
#ifndef ASTRONOMY_H
#define ASTRONOMY_H

#include "astronomy_global.h"
#include "observatory.h"
#include "amzer.h"
#include "sun.h"
#include "moon.h"
#include "planets.h"


/** \class Astronomy
 * \brief <B>Classes for astronomical calculations</B>
 *
 * Adapted from c program skycalc by John Thorstensen, Dartmouth College.
 * 'skycalc version: 6.1, 2005). JFLB  2014/04
 */
//------------------------------------------------------------------------------
class Astronomy {
/**
 * \brief Constructor
 * Gives default values to parameters
 *
 */
public:
    Astronomy();
/**
 * \brief Destructor
 *
 */
public:
     ~Astronomy();

// Parameters
public:
/** \brief Structure defining coordinates in sexigesimal format*/
struct coord
{
/** carry sign explicitly. Values: 1 or -1*/
         short sign;
/** hour or degree part (absolute value) */
         double hh;
/** minute part */
         double mm;
/** second part */
         double ss;
};

// Methods
public:
/** \brief  Computes horizontal coordinates, altitude and azimuth,
 *
 * for declination, hour angle and observatory latitude (decimal degr, hr, degr).
 * Also computes parallactic angle (decimal degr)
 */
   void horizCoord(double dec,double ha,double lat, double *altitude, double *azimuth, double *parangle);

/** \brief Computes the secant of z,
 *
 * assuming the object is not too low to the horizon; returns 100. if the object
 * is low but above the horizon, -100. if the object is just below the horizon.
 */
   double secant_z(double alt);

/** \brief Returns the true airmass for a given secant z.
 *
 * The expression used is based on a tabulation of the mean KPNO atmosphere
 * given by C. M. Snell & A. M. Heiser, 1968, PASP, 80, 336.  They tabulated
 * the airmass at 5 degr intervals from z = 60 to 85 degrees; John Thorstensen
 * fitted the data with a fourth order poly for (secz - airmass) as a function
 * of (secz - 1) using the IRAF curfit routine, then adjusted the zeroth order
 * term to force (secz - airmass) to zero at z = 0.  The poly fit is very close
 * to the tabulated points (largest difference is 3.2e-4) and appears smooth.
 * This 85-degree point is at secz = 11.47, so for secz > 12 it just return
 * secz - 1.5 ... about the largest offset properly determined.
 */
   double true_airmass(double secz);

/** \brief Returns hour angle at which object at dec is at altitude alt.
 *
 *  If object is never at this altitude, signals with special return values 1000
 *  (always higher) and -1000 (always lower).
 */
  double ha_alt(double dec,double lat,double alt);

/** \brief returns radian angle 0 to 2pi for coords x, y -- get that quadrant right !! */
  double atan_circ( double x, double y);

/** \brief Computes minimum and maximum altitude for a given dec and latitude. */
   void min_max_alt(double lat,double decc, double *min_alt, double *max_alt);

/** \brief Angle subtended by two positions in the sky --
 *
 *  Return value is in radians. Hybrid algorithm works down
 *  to zero separation except very near the poles.
 */
  double subtend(double ra1,double dec1,double ra2,double dec2);

/** \brief Returns the local MEAN sidereal time (dec hrs)
 *
 * at julian date jd at west longitude long (decimal hours). Follows
 * definitions in 1992 Astronomical Almanac, pp. B7 and L2. Expression for GMST
 * at 0h ut referenced to Aoki et al, A&A 105, p.359, 1982.  On workstations,
 * accuracy (numerical only!) is about a millisecond in the 1990s.
 */
   double lst(double jd,double longitude);

/** \brief Converts a "babylonian" (sexigesimal) structure
 *  into double-precision floating point ("decimal") number.
 */
   double bab_to_dec( coord bab);

/** \brief Function for converting decimal to babylonian hh mm ss.ss */
   coord dec_to_bab ( double deci);

/** \brief Build a string with coordinate or time in sexigesimal units.
 *
 * Add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
 * Any other value to add nothing.
 */
   string print_time( coord tme, int UT, int secPrec);
/** \brief This is an overloaded member function, provided for convenience.
 *
 * The same with input time/coordinate given in decimal unit: */
   string print_time( double t, int UT, int secPrec);

/** \brief Adjusts a time (decimal hours) to be between -12 and 12,
 *
 * generally used for hour angles.
 */
   double adj_time( double x);

/** \brief Rotates ecliptic rectangular coords x, y, z to equatorial (all assumed of date.) */
   void eclrot( double jd,  double *x,  double *y,  double *z);

/** \brief Assuming x is an angle in degrees, returns modulo 360 degrees. */
   double circulo( double x);

/** \brief Computes the geocentric coordinates from the geodetic
 *
 * (standard map-type) longitude, latitude, and height.
 * These are assumed to be in decimal hours, decimal degrees, and
 * meters respectively. Notation generally follows 1992 Astr Almanac, p. K11.
 */
   void geocent( double geolong, double geolat, double height, double *x_geo, double *y_geo, double *z_geo);

/** \brief Given a julian date in 1900-2100, returns the correction delta t<BR>
 *     TDT - UT (after 1983 and before 1998)<BR>
 *     ET - UT (before 1983)<BR>
 *     an extrapolated guess  (after 2005).
 *
 *  For dates in the past (<= 2001 and after 1900) the value is linearly
 * interpolated on 5-year intervals; for dates after the present, an
 * extrapolation is used, because the true value of delta t cannot be predicted
 * precisely.  Note that TDT is essentially the modern version of ephemeris
 * time with a slightly cleaner definition.
 *
 *  Where the algorithm shifts there will be a small (< 0.1 sec) discontinuity.
 * Also, the 5-year linear interpolation scheme can lead to errors as large as
 * 0.5 seconds in some cases, though usually rather smaller.   One seldom has
 * actual UT to work with anyway, since the commonly-used UTC is tied to TAI
 * within an integer number of seconds.
 */
   double etcorr( double jd);

/** \brief evaluates a polynomial expansion for the approximate brightening of the zenith in twilight
 *
 * (in magnitudes) compared to its value at full night, as function of altitude
 * of the sun (in degrees). To get this expression the author looked in Meinel,
 * A., & Meinel, M., "Sunsets, Twilight, & Evening Skies", Cambridge U. Press,
 * 1983; there's a graph on p. 38 showing the decline of zenith twilight.
 * The author read points off this graph and fit them with a polynomial;
 * the author don't even know what band there data are for!
 * Comparison with Ashburn, E. V. 1952, JGR, v.57, p.85 shows that this is a
 * good fit to his B-band measurements.
 */
   float ztwilight( double alt);

/** \brief Converts cartesian coordinate (x,y,z) to right ascension and declination,
 *
 * returned in decimal hours and decimal degrees.
 */
   void xyz_cel( double x, double y, double z, double *ra, double *dec);

/** \brief Corrects celestial unit vector for aberration due to earth's motion.
 *
 * Uses accurate sun position ... replace with crude one for more speed if needed.<BR>
 *  epoch, decimal year ...<BR>
 *  vec[];   celestial unit vector ...<BR>
 *  from_std;  1 = apply aberration, -1 = take aberration out.<BR>
 */
   void aberrate( double epoch, double vec[3], int from_std);

/** \brief Computes the nutation parameters delta psi and delta epsilon
 *
 * at julian epoch (in years) using approximate formulae given by Jean Meeus,
 * Astronomical Formulae for Calculators, Willman-Bell, 1985, pp. 69-70.
 * Accuracy appears to be a few hundredths of an arcsec or better and numerics
 * have been checked against his example. Nutation parameters are returned in
 * radians.
 */
   void nutation_params( double date_epoch,  double *del_psi,  double *del_ep);

/** \brief General routine for precession and apparent place.
 *
 * Either transforms from current epoch (given by jd) to a standard epoch or
 * back again, depending on value of the switch "from_std":<BR>
 *     1 transforms from standard to current,<BR>
 *    -1 goes the other way.<BR>
 * Optionally does apparent place including nutation and annual aberration
 * (but neglecting diurnal aberration,parallax, proper motion, and GR deflection
 * of light); switch for this is "just_precess",<BR>
 *     1 does only precession,<BR>
 *     0 includes other aberration & nutation.<BR>
 * Precession uses a matrix procedures as outlined in Taff's Computational
 * Spherical Astronomy book. This is the so-called 'rigorous' method which
 * should give very accurate answers all over the sky over an interval of
 * several centuries. Naked eye accuracy holds to ancient times, too. Precession
 * constants used are the new IAU1976 -- the 'J2000' system. Nutation is
 * incorporated into matrix formalism by constructing an approximate nutation
 * matrix and taking a matrix product with precession matrix. Aberration is done
 * by adding the vector velocity of the earth to the velocity of the light ray,
 * not kosher relativistically, but empirically correct to a high order for the
 * angle.<BR>
 * rin, din;   input ra and dec<BR>
 * rout, dout;   output<BR>
 */
   void precess( double rin, double din, double std_epoch, double date_epoch,
              double *rout, double *dout, int just_precess, int from_std);

/** \brief Corrects local equatorial coordinates for refraction
 *
 * if sense == 1 , applies refraction to a true ha and dec;<BR>
 * if sense == -1, de-corrects already refracted coordinates.<BR>
 * The calculation is done by computing xyz coordinates in the horizon system,
 * adding to the vertical component, renormalizing back to a unit vector,
 * rotating to the polar system, and transforming back to ha and dec .... a long
 * way around the barn, but completely general.
 */
   void refract_corr( double *ha, double *dec, double latitude, double *size, int sense);

/** \brief Computes refraction size for a given altitude
 *
 * Almanac for 1992, p. B 62.  Ignores variation in temperature and just assumes
 * T = 20 celsius.<BR>
 *   alt;    altitude in degrees<BR>
 *   elev;   elevation in meters<BR>
 */
   double refract_size( double alt, double  elev);

/** \brief Computes near horizon refraction
 *
 * formula for near horizon, function-ized for iteration ...
 * Almanac 1992, p. B62 -- ignores temperature variation
 */
   double near_hor_refr( double app_alt, double pressure);

/** \brief Algorithm for 3-d Euler rotation into galactic.
 *
 * Perfectly rigorous, and with reasonably accurate input numbers derived from
 * original IAU definition of galactic pole (12 49, +27.4, 1950) and zero of
 * long (at PA 123 deg from pole.)
 */
   void galact( double ra, double dec, double epoch, double *glong, double *glat);

/** \brief Converts ra and dec to ecliptic coords.
 *
 * precesses to current epoch first (and hands current epoch back for printing.)
 * ra in decimal hrs, other coords in dec. deg. */
   void eclipt( double ra, double dec, double epoch, double jd, double *curep, double *eclong, double *eclat);

/** \brief Corrects heliocentric position and velocity to the solar system barycenter.
 *
 * This routine takes the position x,y,z and velocity xdot,ydot,zdot, assumed
 * heliocentric, and corrects them to the solar system barycenter taking into
 * account the nine major planets.  Routine evolved by inserting planetary data
 * (given above) into an earlier, very crude barycentric correction.
 */
   void barycor( double jd, double *x, double *y, double *z,
                 double *xdot, double *ydot, double *zdot);

/** \brief Computes heliocentric correction for time and velocity
 *
 * Finds heliocentric correction for given jd, ra, dec, ha, and lat.
 * tcor is time correction in seconds, vcor velocity in km/s, to be added to
 * the observed values. Input ra and dec assumed to be at current epoch.
 */
   void helcor( double jd, double ra, double dec, double ha, double lat, double elevsea, double *tcor, double *vcor);

/** \brief Computes the correction from bary/helio centric to local standard of rest
 *
 * i.e. (v wrt lsr) = (v helio) + vcor.<BR>
 * velocity of the sun is taken to be 13 km/s toward 1900 coords 18 0 0 +30 0 0
 */
   void lsrcor( double ra, double dec, double epoch, double *vcor);


};

#endif // ASTRONOMY_H
