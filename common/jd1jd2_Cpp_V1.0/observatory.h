#ifndef OBSERVATORY_H
#define OBSERVATORY_H

#include "astronomy.h"
#include "amzer.h"

using namespace std;

/**
 * \brief Observation site parameters
 *
 * <B>Site parameters </B><BR>
 *   Longitude <BR>
 *   Latitude <BR>
 *   Elevation <BR>
 *   Sky magnitudes <BR>
 *<B> Observing conditions parameters</B> <BR>
 *   Moon phase <BR>
 *   Seeing <BR>
 *   Airmass <BR>
 * <B>Time parameters </B><BR>
 *   Julian day <BR>
*/

//-----------------------------------------------------------------------
/** \brief Twilights structure
 *
 * Define twilight times, both nautical (Sun below 12° below horizon) and
 * astronomical (Sun below 18° below horizon)
 * jdetw: Jumian date of evening astronomical twilight
 * jdmtw: Jumian date of morning astronomical twilight
 * twi_to_twi: time interval in day between astronomical twilights (Full darkness)
 * jdetw12: Jumian date of evening nautical twilight
 * jdmtw12: Jumian date of morning nautical twilight
 * twi_to_twi12i: time interval in day between nautical twilights
 */
struct Twilights {
  double jdetw;
  double jdmtw;
  float twi_to_twi;
  double jdetw12;
  double jdmtw12;
  float twi_to_twi12;
} ;
//-----------------------------------------------------------------------
//class Observatory: public Moon{
class Observatory{
public:
  /** \class Observatory
 * \brief Constructor: Set parameters for choosen observation site
 *
 * Predefined sites: <BR>
 * default           Default observatory <BR>
 * Calern            Calern <BR>
 * Pic Du Midi       Pic Du Midi <BR>
 * Toulouse          Toulouse, Jolimont <BR>
 * Hakos             Hakos-Sternwarte, Namibia <BR>
 * Townsville        Townsville ,Australia <BR>
 * New Mexico        New Mexico Skies <BR>
 * Escalquens        Escalquens <BR>
 * Florida           Central Florida <BR>
 * OHP               OHP <BR>
 * Kitt Peak         Kitt Peak [MDM Obs.] <BR>
 * SALT/SAAO         SALT/SAAO, Sutherland, South Africa <BR>
 * La Silla          ESO, Cerro La Silla <BR>
 * Paranal           VLT, Cerro Paranal <BR>
 * Palomar           Palomar Observatory <BR>
 * Cerro Tololo      Cerro Tololo <BR>
 * Las Campanas      Las Campanas Observatory <BR>
 * Mount Hopkins     Mount Hopkins, Arizona <BR>
 * McDonald          McDonald Observatory <BR>
 * Siding Spring     Anglo-Australian Tel., Siding Spring <BR>
 * DAO               DAO, Victoria, BC <BR>
 * Mauna Kea         Mauna Kea, Hawaii <BR>
 * Lick              Lick Observatory <BR>
 * Roque             Roque de los Muchachos <BR>
 * SPM               San Pedro Martir <BR>
 *  <BR>
 */
   Observatory(string siteName);
/**
 * \brief Destructor
 *  <BR>
 */
   ~Observatory();

// Parameters

/** \brief Site name */
   string name;
/** \brief West Longitude (fractional hours) */
   double longitude;
/** \brief Latitude (fractional degrees) */
   double latitude;
/** \brief True elevation above sea level (for absolute location)
 *
 * Elevations: There are two separate elevation parameters specified. <BR>
 *  Variable elevsea is the true elevation above sea level is used (together
 *  with an ellipsoidal earth figure) in determining the observatory's
 *  geocentric coordinates for use in the topocentric correction of the moon's
 *  position and in the calculation of the diurnal rotation part of the
 *  barycentric velocity correction.
 *  (following skycalc, John Thorstensen, Dartmouth College.)
 */
   double elevsea;   // elevation above sea level (for absolute location)
/**  \brief Elevation above the horizon (for rise/set calculations)
 *
 * Elevations: There are two separate elevation parameters specified.  <BR>
 *  Variable elevation is the elevation above the horizon used only in
 *  rise/set calculations and adjusts rise/set times assuming the parameter
 *  is the elevation above flat surroundings (e. g., an ocean).
 *  (following skycalc, John Thorstensen, Dartmouth College.)
 */
   double elevation; // observatory elevation above horizon, meters
/** \brief  Added zenith distance for rise/set due to elevation */
   double horiz;     // added zenith distance for rise/set due to elevation
/** \brief standard time zone offset, hours */
   short stdz;
/** \brief Name of time zone, e. g. Eastern */
   string zone_name;
/** \brief Single-character abbreviation of time zone */
   string zabr;
/** \brief Daylight saving time use
 *
 *  use_dst  = 0 don't use day save time parameter <BR>
 *              1 use USA convention <BR>
 *              2 use Spanish convention <BR>
 *              < 0 Southern hemisphere (reserved, unimplimented) <BR>
 *  (following skycalc, John Thorstensen, Dartmouth College.)
 */
   int use_dst;
/** \brief Sky magnitudes
 *
 *  magnitude per square arc second in 9 visible/near infrared filters
 *  (default values are given in constructor) */
   double magsky[9];

/** \brief  Moon phase */
   double moon_phase;
/** \brief  Seeing  */
   double seeing;
/** \brief  Airmass. */
   double airmass;
/** \brief Julian day */
   double julianDay;

/** \brief define horizon of the site as function of astronomical azimuth
 * (0 at south meridan) */
   #define N_HORIZON  360
   double horizon[N_HORIZON];

/** \brief Finds jd's at which daylight savings time begins and ends.
 *
 * The parameter use_dst allows for a number of conventions, namely:
 *      0 = don't use it at all (standard time all the time)
 *      1 = use USA convention (1st Sun in April to
 *           last Sun in Oct after 1986; last Sun in April before)
 *      2 = use Spanish convention (for Canary Islands)
 *      -1 = use Chilean convention (CTIO).
 *      -2 = Australian convention (for AAT).
 *       Negative numbers denote sites in the southern hemisphere,
 *       where jdb and jde are beginning and end of STANDARD time for
 *       the year.
 *       It's assumed that the time changes at 2AM local time; so
 *       when clock is set ahead, time jumps suddenly from 2 to 3,
 *       and when time is set back, the hour from 1 to 2 AM local
 *       time is repeated.  This could be changed in code if need be.  */
   void find_dst_bounds( int yr, short stdz, int use_dst, double *jdb, double *jde);

/** \brief computes Sun set */
   void sunSetRise(double JDmid, double rasun, double decsun,
		   Observatory *observatory, double horiz, double jdb, double jde,
		   double *jdsunset, double *jdsunrise,
		   float *set_to_rise, double *jdcent);

/** \brief Computes twilights */
   void twilights(double JDmid, double rasun, double decsun,
		  Observatory *observatory, double jdb, double jde,
		  Twilights *twi);
/** \brief Computes evening and morning twilights for given altiude of Sun below horizon */
   Twilights evening_morning_twilights(double alt, double hatwilight,
		double rasun, double JDmid, Observatory *observatory);

/** \brief Print out twilights */
void print_twilights(Twilights twi, double jdb, double jde, double jdcent, Observatory *observatory);
/** \brief Print out Moon coordinates */
void print_Moon_coordinates(double georamoon, double geodecmoon,
			    double toporamoon, double topodecmoon);
/** \brief Print out Sun coordinates */
void print_Sun_coordinates(double rasun, double decsun,
			   double topora, double topodec,
			   double sundist, double x, double y, double z);
/** \brief Read observatory parameters from ascii file */
int read_from_file(string filename, Observatory *observatory, amzer *date,
		   double *ra, double *dec, string *equinoxe, double *min_height, double *Moon_lim );
int get_parameter_from_string(string str, string param, string *value);
int get_parameter_from_string(string str, string param, short *value);
int get_parameter_from_string(string str, string param, int *value);
int get_parameter_from_string(string str, string param, double *value);
int get_parameter_from_string(string str, string param, amzer *date);
};

#endif
