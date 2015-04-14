#ifndef MOON_H
#define MOON_H

#include "astronomy.h"

//*****************************************************************************
/** \class Moon
 *  \brief Class containing methods concerning the Moon */
//------------------------------------------------------------------------------
class Moon{
/** \brief Constructor */
public:
   Moon();
/** \brief Destructor */
public:
   ~Moon();

// Parameters
public:

  /** \brief Geocentric equatorial coordinates of the Moon: right ascension  (decimal hours) */
  double geora;
  /** \brief Geocentric equatorial coordinates of the Moon: right declination (decimal degrees)*/
  double geodec;
  /** \brief Geocentric distance of the Moon    (earth radii*/
  double geodist;
  /** \brief Topocentric equatorial coordinates of the Moon: right ascension  (decimal hours) */
  double topora;
  /** \brief Topocentric equatorial coordinates of the Moon: right declination (decimal degrees)*/
  double topodec;
  /** \brief Topocentric distance of the Moon    (earth radii)*/
  double topodist;

// Methods
public:

/** \brief More accurate (but more elaborate and slower) lunar ephemeris
 *
 *  from Jean Meeus' *Astronomical Formulae For Calculators*,
 *  pub. Willman-Bell.  Includes all the terms given there.
 * inputs units:geolat in decimal degrees, lst in decimal hours., elevsea in meters
 */
   void accumoon( double JD, double geolat, double lst, double elevsea, Moon *moon);

/** \brief Gives jd (+- 2 min) of phase nph on lunation n.
 *
 * This routine implements formulae found in Jean Meeus' *Astronomical Formulae
 * for Calculators*, 2nd edition, Willman-Bell. A very usefulbook!!
 * n, nph lunation and phase; nph = 0 new, 1 1st, 2 full, 3 last
 * jdout   jd of requested phase
 */
   void flmoon( int n, int nph, double *jdout);

/** \brief Compute age in days of moon since last new, and lunation of last new moon. */
   float lun_age( double jd,  int *nlun);

/** \brief Prints a verbal description of moon phase, given the julian date.*/
   string print_phase( double jd);

/** \brief Evaluates predicted LUNAR part of sky brightness,
 *
 * in V magnitudes per square arcsecond,
 * following K. Krisciunas and B. E. Schaeffer (1991) PASP 103, 1033.
 *
 *  alpha = separation of sun and moon as seen from earth,
 *  converted internally to its supplement, <BR>
 *  rho = separation of moon and object, <BR>
 *  kzen = zenith extinction coefficient, <BR>
 *  altmoon = altitude of moon above horizon, <BR>
 *  alt = altitude of object above horizon <BR>
 *  moondist = distance to moon, in earth radii <BR>
 *  all are in decimal degrees.
 */
   double lunskybright(  double alpha,  double rho,  double kzen,  double altmoon,  double alt,   double moondist);

/** \brief Returns jd at which moon is at a given altitude,
 *
 * given jdguess as a starting point. In current version uses high-precision
 * moon -- execution time does not seem to be excessive on modern hardware.
 * If it's a problem on your machine, you can replace calls to 'accumoon' with
 * 'lpmoon' and remove the 'elevsea' argument.
 */
   double jd_moon_alt( double alt, double jdguess, double lat, double longit, double elevsea);

};

//------------------------------------------------------------------------------
#endif

