#ifndef PLANETS_H
#define PLANETS_H

#include "astronomy.h"

using namespace std;

//*****************************************************************************
/** \class Planets
 *
 * \brief Classe defining planets
 *
 * Adapted from c program skycalc by John Thorstensen, Dartmouth College.
 * JFLB  2009/07
 *
 * Planetary part. The intention of this is to compute low-precision planetary
 * positions for general info and to inform user if observation might be
 * interfered with by a planet -- a rarity, but it happens.  Also designed to
 * make handy low-precision planet positions available for casual planning
 * purposes. Do not try to point blindly right at the middle of a planetary disk
 * with these routines!
 */
//------------------------------------------------------------------------------
class Planets
{
/** \brief Constructor */
public:
   Planets();
/** \brief Destructor */
public:
   ~Planets();

// Parameters
public:
/** \brief Structure defining elements of planetary orbits */
struct planetary_elements {
/** \brief Name of the planet */
   string name;
/** \brief Inclination of the orbit */
   double incl;
/** \brief Longitude of the ascending node of the orbit */
   double Omega;
/** \brief Longitude of the perihelion of the orbit */
   double omega;
/** \brief Semimajor axis of the orbit */
   double a;
/** \brief daily motion */
   double daily;
/** \brief Eccentricity of the orbit */
   double ecc;
/** \brief Mean longitude */
   double L_0;
/** \brief Mass of the planet */
   double mass;
};
planetary_elements el[10];
double jd_el;

// Methods
public:

/** \brief Computes and loads mean elements for planets. */
void comp_el( double jd);

/** \brief Produces ecliptic x,y,z coordinates for planet number 'p' at date jd.
 *
 * see 1992 Astronomical Almanac, p. E 4 for these formulae.
 */
void planetxyz( int p, double jd, double *x, double *y, double *z);

/** \brief Numerically evaluates planet velocity by brute-force
 *
 * numerical differentiation. Very unsophisticated algorithm.
 */
void planetvel( int p, double jd, double *vx, double *vy, double *vz);

/** \brief Simply transforms a vector x, y, and z to 2000 coordinates and prints
 *
 * for use in diagnostics. answer should be in ecliptic coordinates, in AU per day.
 */
string xyz2000( double jd ,double *x, double *y, double *z);

/** \brief Simply transforms a vector x, y, and z to 2000 coordinates
 *
 * and hands it back through pointers.  For really transforming it!
 */
void xyz2000xf( double jd, double *x, double *y, double *z);

/** \brief Computes ra and dec of i-th planet as viewed from earth.
 *
 * Given computed planet positions for planets 1-10, computes
 * ra and dec of i-th planet as viewed from earth (3rd);
 */
void earthview( double *x, double *y, double *z, int i, double *ra, double *dec);


};

//------------------------------------------------------------------------------
#endif
