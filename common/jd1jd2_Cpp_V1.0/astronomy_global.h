#ifndef ASTRONOMY_GLOBAL_H
#define ASTRONOMY_GLOBAL_H

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>      // std::ifstream
#include <iomanip>
#include <string.h>
#include <string>
#include <sstream>
using namespace std;

#define XFORM_FROMSTD  1  // defined quantities for apparent place transforms
#define XFORM_TOSTDEP  -1
#define XFORM_JUSTPRE  1
#define XFORM_DOAPPAR  0

// some (not all) physical, mathematical, and astronomical constants
//   used are defined here.

#define  PI                3.14159265358979
#define  TWOPI             6.28318530717959
#define  PI_OVER_2         1.57079632679490  // From Abramowitz & Stegun
#define  ARCSEC_IN_RADIAN  206264.8062471
#define  DEG_IN_RADIAN     57.2957795130823
#define  HRS_IN_RADIAN     3.819718634205
#define  KMS_AUDAY         1731.45683633     // km per sec in 1 AU/day
#define  SPEED_OF_LIGHT    299792.458        // in km per sec ... exact.
#define  SS_MASS           1.00134198        // solar system mass in solar units
#define  J2000             2451545.          // Julian date at standard epoch
#define  SEC_IN_DAY        86400.
#define  FLATTEN           0.003352813       // flattening of earth, 1/298.257
#define  EQUAT_RAD         6378137.          // equatorial radius of earth, meters
#define  ASTRO_UNIT        1.4959787066e11   // 1 AU in meters
#define  RSUN              6.96000e8         // IAU 1976 recom. solar radius, meters
#define  RMOON             1.738e6           // IAU 1976 recom. lunar radius, meters
#define  FIRSTJD           2415387.          // 1901 Jan 1 -- calendrical limit
#define  LASTJD            2488070.          // 2099 Dec 31

#define  EARTH_DIFF        0.05            // used in numerical
//   differentiation to find earth velocity -- this value gives
//   about 8 digits of numerical accuracy on the VAX, but is
//   about 3 orders of magnitude larger than the value where roundoff
//   errors become apparent.


#endif // ASTRONOMY_GLOBAL_H
