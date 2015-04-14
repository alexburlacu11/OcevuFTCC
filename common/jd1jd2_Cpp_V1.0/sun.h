#ifndef SUN_H
#define SUN_H

#include "astronomy.h"

//*****************************************************************************
/** \class Sun
 * \brief Class containing methods concerning the Sun */
//------------------------------------------------------------------------------
class Sun{
/** \brief Constructor */
public:
   Sun();
/** \brief Destructor */
public:
   ~Sun();

   // Parameters
public:

  /** \brief Geocentric equatorial coordinates of the Sun: right ascension  (decimal hours) */
  double ra;
  /** \brief Geocentric equatorial coordinates of the Sun: right declination (decimal degrees)*/
  double dec;
  /** \brief Geocentric distance of the Sun    (earth radii*/
  double dist;
  /** \brief Topocentric equatorial coordinates of the Sun: right ascension  (decimal hours) */
  double topora;
  /** \brief Topocentric equatorial coordinates of the Sun: right declination (decimal degrees)*/
  double topodec;
  /** \brief x, y, and z are heliocentric equatorial coordinates of the
   *  EARTH, referred to mean equator and equinox of date. */
  double x, y, z;

// Methods
public:

/** \brief Low precision formulae for the sun,
 *
 * from Almanac p. C24 (1990) <BR>
 * ra and dec are returned as decimal hours and decimal degrees.
 */
   void lpsun( double jd, double *ra, double *dec);

/** \brief More accurate solar ephemeris.
 *
 * Implemenataion of Jean Meeus' more accurate solar ephemeris. <BR>
 * For ultimate use in helio correction!
 * From Astronomical Formulae for Calculators, pp. 79 ff.
 * This gives sun's position wrt *mean* equinox of date, not *apparent*.
 * Accuracy is << 1 arcmin.  Positions given are geocentric.
 * Parallax due to observer's position on earth is ignored. This is up to
 * 8 arcsec; Routine is usually a little better than that. <BR>
 *      // -- topocentric correction *is* included now. -- // <BR>
 * Light travel time is apparently taken into account for the ra and dec, but
 * the author don't know if aberration is and he don't know if distance is
 * simlarly antedated.
 *
 * x, y, and z are heliocentric equatorial coordinates of the
 * EARTH, referred to mean equator and equinox of date.
 */
  void accusun( double jd, double lst, double geolat, Sun *sun);

/** \brief Returns jd at which sun is at a given altitude,
 *
 * given jdguess as a starting point. <BR>
 * Uses low-precision sun, which is plenty good enough.
 */
   double jd_sun_alt( double alt, double jdguess, double lat, double longit);

};

//------------------------------------------------------------------------------
#endif
