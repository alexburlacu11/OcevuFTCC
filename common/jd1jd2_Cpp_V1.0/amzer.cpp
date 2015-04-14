#include "amzer.h"

// Class containing parameter values and methods defining a time.
//------------------------------------------------------------------------------
// Constructor
amzer::amzer()
{
    JD = 2454000.0;
    JD2calendar();
}

//------------------------------------------------------------------------------
// Destructor
amzer::~amzer()
{
}

//------------------------------------------------------------------------------
double cal2JD( int day, int month, int year, int hour, int min, double second)
{
   int annee;
   int mois;
   if (month==1 || month==2)
   {
     annee=year-1;
     mois=month+12;
   } else {
     annee=year;
     mois=month;
   }
   double a = floor( (double)annee/100.0 );
   double JD = 2.0 - a + floor(a/4.0) + floor(365.25*(double)annee)+
        floor( 30.6001 *( (double)mois+1.0)) + (double)day+1720994.5 +
        (double)hour/24.0+(double)min/1440.0+second/86400.0;
   return JD;
}

//------------------------------------------------------------------------------
void amzer::calendar2JD()
{
   JD = cal2JD( day, month, year, hour, min, second);
}

//------------------------------------------------------------------------------
void amzer::JD2calendar()
{
  double jdfrac =  JD + 0.5 - floor(JD+ 0.5);
  hour = floor( jdfrac*24 );
  min = floor( (jdfrac*24 - hour) *60 );
  second = ( jdfrac*24 - hour )*3600 - min*60;

  double igreg = 2299161.0;
  double jdint = floor(JD+ 0.5);
  double ja;
  if( jdint>=igreg )
  {
        double jalpha = floor(((jdint-1867216.0)-0.25)/36524.25);
        ja = jdint + 1.0 + jalpha - floor(0.25*jalpha);
  } else {
        ja=jdint;
  }
  double jb = ja + 1524.0;
  double jc = floor(6680.0+((jb-2439870.0)-122.1)/365.25);
  double jd = 365.0*jc+floor(0.25*jc);
  double je = floor((jb-jd)/30.6001);
  double id = jb-jd-floor(30.6001*je);
  double mm = je - 1.0;
  if( mm>12.0 ) mm = mm - 12.0;
  double iyyy = jc - 4715.0;
  if( mm>2.0 ) iyyy = iyyy-1.0;
  if( iyyy<=0.0 ) iyyy = iyyy-1.0;
  year = (int)iyyy;
  month = (int)mm;
  day = (int)id;

}

// ---------------------------------------------------------------------------------
// returns day of week for a jd, 0 = Mon, 6 = Sun.
int amzer::day_of_week()
{
  double x = floor(JD+0.5)/7.+0.01;
  double d = 7.0*(x - floor(x));
  return(d);
}

// ---------------------------------------------------------------------------------
// returns day of year.
double amzer::day_of_year()
{
   JD2calendar();
   // find julian date of "jan 0" = Dec 31 of previous year
   int y = year - 1;
   int mo = 12;
   int d = 31;
   int h = 0;
   int mi = 0;
   double s = 0.;
   double julday = cal2JD( d, mo, y, h, mi, s);

   return( JD - julday );
}

// ---------------------------------------------------------------------------------
// prints day of week given number 0=Mon,6=Sun
string amzer::print_day(int d)
{
  string days = "MonTueWedThuFriSatSun";
  string day_out = "   ";
  for(int i=0; i<3; i++) day_out[i] = days[3*d+i];
  return day_out;
}
// ---------------------------------------------------------------------------------
string amzer::print_all(int UT, int secPrec)
{
  // day of week
  int dow = day_of_week();
  string day_out = print_day(dow);
  // month name
  string months = "JanFebMarAprMayJunJulAugSepOctNovDec";
  string mo_out = "   ";
  for(int i=0; i<3; i++) mo_out[i] = months[3*(month-1)+i];

  ostringstream oss;
  string dateStr;
  oss << day_out << " " << day << " "  << mo_out << " "  << year
      << " " << hour << ":"  << min << ":" << fixed << setprecision (secPrec) << second;
  dateStr=oss.str();
//  add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
  if( UT == 0)
  {
    dateStr = dateStr +" local time";
  } else if( UT == 1) {
    dateStr = dateStr + " UT";
  }
  return dateStr;
}
// ---------------------------------------------------------------------------------
string amzer::print_calendar()
{
  // day of week
  int dow = day_of_week();
  string day_out = print_day(dow);
  // month name
  string months = "JanFebMarAprMayJunJulAugSepOctNovDec";
  string mo_out = "   ";
  for(int i=0; i<3; i++) mo_out[i] = months[3*(month-1)+i];

  ostringstream oss;
  string dateStr;
  oss << day_out << " " << day << " "  << mo_out << " "  << year;
  dateStr=oss.str();
  return dateStr;
}
// ---------------------------------------------------------------------------------
string amzer::print_time(int UT, int secPrec)
{
  ostringstream oss;
  string dateStr;
  oss << hour << ":"  << min << ":" << fixed << setprecision (secPrec) << second;
  dateStr=oss.str();
//  add a statement of whether time is "local" (UT=0)  or "ut" (UT=1)
  if( UT == 0)
  {
    dateStr = dateStr +" local time";
  } else if( UT == 1) {
    dateStr = dateStr + " UT";
  }
  return dateStr;
}

// ---------------------------------------------------------------------------------
// Returns zone time offset when standard time zone is stdz,
// when daylight time begins (for the year) on jdb, and ends (for the year)
// on jde. Specifying a negative value of use_dst reverses the logic for the
// Southern hemisphere; then DST is assumed for the Southern hemisphere summer
// (which is the end and beginning* of the year.
double amzer::zone( int use_dst, double stdz, double jd, double jdb, double jde)
{
   if(use_dst == 0)
     return(stdz);
   else if((jd > jdb) && (jd < jde) && (use_dst > 0))
     return(stdz-1.);
   else if(((jd < jdb) || (jd > jde)) && (use_dst < 0))
     return(stdz-1.);
   else
     return(stdz);
}


// ---------------------------------------------------------------------------------

