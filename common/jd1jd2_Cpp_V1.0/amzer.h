#ifndef AMZER_H
#define AMZER_H


#include "astronomy_global.h"

using namespace std;

/** \class amzer
 * \brief Class containing parameters and methods defining a time.
 */
//-----------------------------------------------------------------------
class amzer{
public:
/** \brief Constructor */
   amzer();      //Constructor
/** \brief Destructor */
   ~amzer();     //Destructor

// Parameters

/** \brief Julian date */
   double JD;
/** \brief day part */
   int day;
/** \brief month part */
   int month;
/** \brief year part */
   int year;
/** \brief hour  part */
   int hour;
/** \brief minute part */
   int min;
/** \brief second part */
   double second;

// Methods

/** \brief Computes calendar date for a given julian date */
   void JD2calendar();

/** \brief Computes julian date for a given calendar date */
   void calendar2JD();

/** \brief returns day of week for a jd, 0 = Mon, 6 = Sun. */
int day_of_week();

/** \brief returns day of year */
double day_of_year();

/** \brief Prints in a string day of week given number 0=Mon,6=Sun */
string print_day(int d);

/** \brief Prints time in a string: year, month, day, hour, minute, second
 *
 *  add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
 */
string print_all(int UT, int secPrec);

/** \brief Prints in a string a year, month, day. */
string print_calendar();

/** \brief Prints time (h m s) in a string
 *
 *  add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
 */
string print_time(int UT, int secPrec);

/** \brief Returns zone time offset when standard time zone is stdz,
 *
 * when daylight time begins (for the year) on jdb, and ends (for the year)
 * on jde. Specifying a negative value of use_dst reverses the logic for the
 * Southern hemisphere; then DST is assumed for the Southern hemisphere summer
 * (which is the end and beginning* of the year.
 */
double zone( int use_dst, double stdz, double jd, double jdb, double jde);

};

#endif
//#ifndef AMZER_H
//#define AMZER_H
