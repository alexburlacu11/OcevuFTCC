#include "observatory.h"

//------------------------------------------------------------------------------
//Observatory parameter values.
//
//  Site parameters:
//  * Longitude
//  * Latitude
//  * Elevation
//  * Sky magnitudes
//  Observing conditions parameters:
//  * Moon phase
//  * Seeing
//  * Airmass
//  Time parameters:
//  * Julian day
//------------------------------------------------------------------------------
// Constructor: Set parameters for choosen observation site
Observatory::Observatory(string siteName)
{
  name = "Default observatory";
  longitude = 0.0;
  latitude = 44.0;
  elevsea = 0.0;
  elevation = 0.0;
  horiz = 0.0;
  stdz = 0.0;
  zone_name = "-";
  zabr = "-";
  use_dst = 0;
  magsky[0] = 22.0; // U
  magsky[1] = 22.7; // B
  magsky[2] = 21.8; // V
  magsky[3] = 20.9; // R
  magsky[4] = 19.9; // I
  magsky[5] = 18.5; // Y
  magsky[6] = 16.0; // J
  magsky[7] = 14.4; // H
  magsky[8] = 13.3; // K
  moon_phase = 0.0;
  seeing = 0.5;
  airmass = 1.0;
  julianDay = 2446492.0;
  for(int i=0; i<N_HORIZON; i++) horizon[i]=0.0;

//  else if( siteName == "" )
//  {
//      name = "";
//      zone_name = "Greenwich";
//      zabr = 'G';
//      use_dst = 0;
//      longitude = ;
//      latitude = ;
//      stdz = 0;
//      elevsea = ;
//      elevation = ;
//  }

// "default"           "Default observatory"
// "Calern"            "Calern"
// "Pic Du Midi"       "Pic Du Midi"
// "Toulouse"          "Toulouse, Jolimont"
// "New Mexico"        "New Mexico Skies"
// "OHP"               "OHP"
// "Kitt Peak"         "Kitt Peak [MDM Obs.]"
// "SALT/SAAO"         "SALT/SAAO, Sutherland, South Africa"
// "La Silla"          "ESO, Cerro La Silla"
// "Paranal"           "VLT, Cerro Paranal"
// "Palomar"           "Palomar Observatory"
// "Cerro Tololo"      "Cerro Tololo"
// "Las Campanas"      "Las Campanas Observatory"
// "Mount Hopkins"     "Mount Hopkins, Arizona"
// "McDonald"          "McDonald Observatory"
// "Siding Spring"     "Anglo-Australian Tel., Siding Spring"
// "DAO"               "DAO, Victoria, BC"
// "Mauna Kea"         "Mauna Kea, Hawaii"
// "Lick"              "Lick Observatory"
// "Roque"             "Roque de los Muchachos"
// "SPM"               "San Pedro Martir"

  if( siteName == "" || siteName == "default" )
  {
    name = "Default observatory";
    longitude = 0.0;
    latitude = 0.0;
    elevsea = 0.0;
    elevation = 0.0;
    horiz = 0.0;
    stdz = 0.0;
    zone_name = "-";
    zabr = "-";
    use_dst = 0;
    magsky[0] = 22.0; // U
    magsky[1] = 22.7; // B
    magsky[2] = 21.8; // V
    magsky[3] = 20.9; // R
    magsky[4] = 19.9; // I
    magsky[5] = 18.5; // Y
    magsky[6] = 16.0; // J
    magsky[7] = 14.4; // H
    magsky[8] = 13.3; // K

    moon_phase = 0.0;
    seeing = 0.5;
    airmass = 1.0;
    julianDay = 2454666.0;
    for(int i=0; i<N_HORIZON; i++) horizon[i]=0.0;
  }

  else if( siteName == "Calern" )
  {
      name = "Calern";
      zone_name = "Greenwich";
      zabr = 'G';
      use_dst = 0;
      longitude = -0.4615927;
      latitude = 43.75222;
      stdz = 0;
      elevsea = 1270.;
      elevation = 1270.;
  }

  // Bagnères-de-Bigorre, Hte Pyrenées      -0°08.7'     +42°56.2'      2861m
  else if( siteName == "Pic Du Midi" || siteName == "PicDuMidi")
  {
      name = "Pic Du Midi";
      zone_name = "Greenwich";
      zabr = 'G';
      use_dst = 0;
      longitude = -0.0096667;
      latitude = 42.936667;
      stdz = 0;
      elevsea = 2800.;
      elevation = 2800.;
  }

  //   Obs. de Toulouse, Jolimont   -1°27.8'     +43°36.7'       195m
  else if( siteName == "Toulouse" )
  {
      name = "Toulouse";
      zone_name = "Greenwich";
      zabr = 'G';
      use_dst = 0;
      longitude = -0.097556;
      latitude = 43.611667;
      stdz = 0;
      elevsea = 195.;
      elevation = 195.;
  }

  //   New Mexico Skies Lat. 32° 54' 14" Long. 105° 31' 44", Elev. 7,300 feet/2,225 meters
  else if( siteName == "New Mexico" )
  {
      name = "New Mexico Skies";
      zone_name = "USACentral";
      zabr = 'C';
      use_dst = 1;
      longitude = 7.035259;
      latitude = 32.903889;
      stdz = 7.;
      elevsea = 2225.;
      elevation = 2225.;
  }

  // OHP  latitude 43.9317  logngitude -5.7133 W deg.
  else if( siteName == "OHP" )
  {
      name = "OHP";
      zone_name = "Greenwich";
      zabr = 'G';
      use_dst = 0;
      longitude = -5.7133;
      latitude = 43.9317;
      stdz = 0;
      elevsea = 650.;
      elevation = 650.;
  }

  else if( siteName == "Kitt Peak" )
  {
      name = "Kitt Peak [MDM Obs.]";
      zone_name = "Mountain";
      zabr = 'M';
      use_dst = 0;
      longitude = 7.44111;     // decimal hours
      latitude = 31.9533;      // decimal degrees
      stdz = 7.;
      elevsea = 1925.;         // for MDM observatory, strictly
      elevation = 700.;        // approximate -- to match KPNO tables
  }
  else if( siteName == "SALT/SAAO" )
  {
      name =  "SALT/SAAO, Sutherland";
      zone_name = "South African";
      zabr = 'S';
      use_dst = 0;
      longitude = -1.38744;
      latitude = -32.3783;
      stdz = -2;
      elevsea = 1771.;
      elevation = 1771.;      // guess!
  }
  else if( siteName == "La Silla" )
  {
      name =  "ESO, Cerro La Silla";
      zone_name = "Chilean";
      zabr = 'C';
      use_dst = -1;
      longitude = 4.7153;
      latitude = -29.257;
      stdz = 4.;
      elevsea = 2347.;
      elevation = 2347.;     // for ocean horizon, not Andes!
      cout << endl << "Will use daylight time, Chilean date conventions." << endl << endl;
  }
  else if( siteName == "Paranal" )
  {
      name =  "VLT, Cerro Paranal";
      zone_name = "Chilean";
      zabr = 'C';
      use_dst = -1;
      longitude = 4.69356;
      latitude = -24.625;
      stdz = 4.;
      elevsea = 2635.;
      elevation = 2635.;     // for ocean horizon, not Andes!
      cout << endl << "Will use daylight time, Chilean date conventions." << endl << endl;
  }
  else if( siteName == "Palomar" )
  {
      name =  "Palomar Observatory";
      zone_name = "Pacific";
      zabr = 'P';
      use_dst = 1;
      longitude = 7.79089;
      latitude = 33.35667;
      elevsea = 1706.;
      elevation = 1706.;      // not clear if it's appropriate ...
      stdz = 8.;
  }
  else if( siteName == "Cerro Tololo" )
  {
      name =  "Cerro Tololo";
      zone_name = "Chilean";
      zabr = 'C';
      use_dst = -1;
      longitude = 4.721;
      latitude = -30.165;
      stdz = 4.;
      elevsea = 2215.;
      elevation = 2215.;     // for ocean horizon, not Andes!
      cout << endl << "Will use daylight time, Chilean date conventions." << endl << endl;
  }
  else if( siteName == "Las Campanas" )
  {
      name =  "Las Campanas Observatory";
      zone_name = "Chilean";
      zabr = 'C';
      use_dst = -1;
      longitude = 4.71333;
      latitude = -29.00833;
      stdz = 4.;
      elevsea = 2282.;
      elevation = 2282.;     // for ocean horizon, not Andes!
      cout << endl << "Will use daylight time, Chilean date conventions." << endl << endl;
  }
  else if( siteName == "Mount Hopkins" )
  {
      name =  "Mount Hopkins, Arizona";
      zone_name = "Mountain";
      zabr = 'M';
      use_dst = 0;
      longitude = 7.39233;
      latitude = 31.6883;
      elevsea = 2608.;
      elevation = 500.;      // approximate elevation above horizon mtns
      stdz = 7.;
  }
  else if( siteName == "McDonald" )
  {
      name = "McDonald Observatory";
      zone_name = "Central";
      zabr = 'C';
      use_dst = 1;
      longitude = 6.93478;
      latitude = 30.6717;
      elevsea = 2075;
      elevation = 1000.;      // who knows?
      stdz = 6.;
       }
  else if( siteName == "Siding Spring" )
  {
      name =  "Anglo-Australian Tel., Siding Spring";
      zone_name = "Australian";
      zabr = 'A';
      use_dst = -2;
      longitude = -9.937739;
      latitude = -31.277039;
      elevsea = 1149.;
      elevation = 670.;
      stdz = -10.;
  }
  else if( siteName == "DAO" )
  {
      name =  "DAO, Victoria, BC";
      zone_name = "Pacific";
      zabr = 'P';
      use_dst = 1;
      cout << endl << "WARNING: United States conventions for DST assumed." << endl << endl;
      longitude = 8.22778;
      latitude = 48.52;
      elevsea = 74.;
      elevation = 74.;      // not that it makes much difference
      stdz = 8.;
  }
  else if( siteName == "Mauna Kea" )
  {
      name =  "Mauna Kea, Hawaii";
      zone_name = "Hawaiian";
      zabr = 'H';
      use_dst = 0;
      longitude = 10.36478;
      latitude = 19.8267;
      elevsea = 4215.;
      elevation = 4215.;      // yow!
      stdz = 10.;
  }
  else if( siteName == "Lick" )
  {
      name =  "Lick Observatory";
      zone_name = "Pacific";
      zabr = 'P';
      use_dst = 1;
      longitude = 8.10911;// "Escalquens"        "Escalquens"
      // "Florida"           "Central Florida"

      latitude = 37.3433;
      elevsea = 1290.;
      elevation = 1290.;     // for those nice Pacific sunsets
      stdz = 8.;
  }
  else if( siteName == "Roque" )
  {
      name =  "Roque de los Muchachos";
      zone_name = "pseudo-Greenwich";
      zabr = 'G';
      use_dst = 2;
      longitude = 1.192;
      latitude = 28.75833;
      elevsea = 2326.;
      elevation = 2326.;
      stdz = 0.;
  }
  else if( siteName == "SPM" || siteName == "San Pedro Martir")
  {
    name =  "San Pedro Martir";
    zone_name = "Pacific";
    zabr = 'P';
    use_dst = 1;
    longitude = 7.697553;
    latitude = 31.03667;
    elevsea = 2800.0;
    elevation = 2800.0;
    stdz = 8.;
  }

}

//------------------------------------------------------------------------------
// Destructor
Observatory::~Observatory()
{
}

//------------------------------------------------------------------------------
// Returns jd's at which daylight savings time begins and ends.
// The parameter use_dst allows for a number of conventions, namely:
//       0 = don't use it at all (standard time all the time)
//       1 = use USA convention (1st Sun in April to
//            last Sun in Oct after 1986; last Sun in April before)
//       2 = use Spanish convention (for Canary Islands)
//       -1 = use Chilean convention (CTIO).
//       -2 = Australian convention (for AAT).
//        Negative numbers denote sites in the southern hemisphere,
//        where jdb and jde are beginning and end of STANDARD time for
//        the year.
//        It's assumed that the time changes at 2AM local time; so
//        when clock is set ahead, time jumps suddenly from 2 to 3,
//        and when time is set back, the hour from 1 to 2 AM local
//        time is repeated.  This could be changed in code if need be. */
void Observatory::find_dst_bounds( int yr, short stdz, int use_dst, double *jdb, double *jde)
{
  amzer trial;

  if((use_dst == 1) || (use_dst == 0))
  {
    /* USA Convention, and including no DST to be defensive */
    /* Note that this ignores various wrinkles such as the
     *      brief Nixon administration flirtation with year-round DST,
     *      the extended DST of WW II, and so on. */
    trial.year = yr;
    trial.month = 4;
    if(yr >= 1986) trial.day = 1;
    else trial.day = 30;
    trial.hour = 2;
    trial.min = 0;
    trial.second = 0;

    /* Find first Sunday in April for 1986 on ... */
    if(yr >= 1986)
    {
      trial.calendar2JD();
      while(trial.day_of_week() != 6)
      {
	trial.day++;
	trial.calendar2JD();
      }
    }
    /* Find last Sunday in April for pre-1986 .... */
    else
    {
      trial.calendar2JD();
      while(trial.day_of_week() != 6)
      {
	trial.day--;
	trial.calendar2JD();
      }
    }

    trial.calendar2JD();
    *jdb = trial.JD + stdz/24.;

    /* Find last Sunday in October ... */
    trial.month = 10;
    trial.day = 31;
    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day--;
      trial.calendar2JD();
    }
    *jde = trial.JD + (stdz - 1.)/24.;
  }
  else if (use_dst == 2) {  /* Spanish, for Canaries */
    trial.year = yr;
    trial.month = 3;
    trial.day = 31;
    trial.hour = 2;
    trial.min = 0;
    trial.second = 0;

    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day--;
      trial.calendar2JD();
    }
    *jdb = trial.JD + stdz/24.;
    trial.month = 9;
    trial.day = 30;
    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day--;
      trial.calendar2JD();
    }
    *jde = trial.JD + (stdz - 1.)/24.;
  }
  else if (use_dst == -1) {  /* Chilean, for CTIO, etc.  */
    /* off daylight 2nd Sun in March, onto daylight 2nd Sun in October */
    trial.year = yr;
    trial.month = 3;
    trial.day = 8;  /* earliest possible 2nd Sunday */
    trial.hour = 2;
    trial.min = 0;
    trial.second = 0;

    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day++;
      trial.calendar2JD();
    }
    *jdb = trial.JD + (stdz - 1.)/24.;
    /* note jdb is beginning of STANDARD time in south,
     *            hence use stdz - 1. */
    trial.month = 10;
    trial.day = 8;
    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day++;
      trial.calendar2JD();
    }
    *jde = trial.JD + stdz /24.;
  }
  else if (use_dst == -2) {  /* For Anglo-Australian Telescope  */
    /* off daylight 1st Sun in March, onto daylight last Sun in October */
    trial.year = yr;
    trial.month = 3;
    trial.day = 1;  /* earliest possible 1st Sunday */
    trial.hour = 2;
    trial.min = 0;
    trial.second = 0;

    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day++;
      trial.calendar2JD();
    }
    *jdb = trial.JD + (stdz - 1.)/24.;
    /* note jdb is beginning of STANDARD time in south,
     *            hence use stdz - 1. */
    trial.month = 10;
    trial.day = 31;
    trial.calendar2JD();
    while(trial.day_of_week() != 6) {
      trial.day--;
      trial.calendar2JD();
    }
    *jde = trial.JD + stdz /24.;
  }
}

//------------------------------------------------------------------------------
// computes Sun set and rise
void Observatory::sunSetRise(double JDmid, double rasun, double decsun,
			     Observatory *observatory, double horiz, double jdb, double jde,
			     double *jdsunset, double *jdsunrise,
			     float *set_to_rise, double *jdcent)
{

  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();
  // Creates the Sun
  Sun *sun = new Sun();

  double hasunset;
  double stmid = astronomy->lst( JDmid, observatory->longitude);
  amzer t;

  // Hour angle when Sun sets or rises
  hasunset = astronomy->ha_alt(decsun,latitude,-(0.83+horiz));
  if(hasunset > 900.)   /* flag for never sets */
  {
    cout << "Sun up all night!" << endl;
    *set_to_rise = 0.;
    *jdcent = -1.;
  }
  else if(hasunset < -900.)
  {
    cout << "Sun down all day!" << endl;
    *set_to_rise = 24.;
    *jdcent = -1.;
  }
  else
  {
    *jdsunset = JDmid + astronomy->adj_time(rasun+hasunset-stmid)/24.;  /* initial guess */
    *jdsunset = sun->jd_sun_alt(-(0.83+horiz),*jdsunset,observatory->latitude,observatory->longitude);

    *jdsunrise = JDmid + astronomy->adj_time(rasun-hasunset-stmid)/24.;
    *jdsunrise = sun->jd_sun_alt(-(0.83+horiz),*jdsunrise,observatory->latitude,observatory->longitude);

    if((*jdsunrise > 0.) && (*jdsunset > 0.)) {
      *set_to_rise = (*jdsunrise - *jdsunset) * 24.;
      *jdcent = (*jdsunrise + *jdsunset) / 2.;
    }
    else {
      cout << " Sunrise not correctly computed.";
      *jdcent = -1.;
    }

  }
  // destroy the Sun
  delete sun;
  // Forget astronomy
  delete astronomy;

}
//------------------------------------------------------------------------------
// Computes twilights
void Observatory::twilights(double JDmid, double rasun, double decsun,
			    Observatory *observatory, double jdb, double jde,
			    Twilights *twi)
{

  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();
  // Creates the Sun
  Sun *sun = new Sun();

  twi->jdetw = -99.0;
  twi->jdmtw = -99.0;
  twi->jdetw12 = -99.0;
  twi->jdmtw12 = -99.0;

  double hatwilight;

  /* Checks for 18-degree twilight as appropriate. */
  hatwilight = astronomy->ha_alt(decsun,observatory->latitude,-18.);
  if(hatwilight < -900.) {
    twi->twi_to_twi = 24.; /* certainly no 12-degree twilight either */
  }
  else if(hatwilight > 900.) {
    twi->twi_to_twi = 0.;  /* but maybe 12-degree twilight occurs ...*/
  }
  else
  {
    *twi = observatory->evening_morning_twilights(-18.0, hatwilight, rasun, JDmid, observatory);
  }

  /* Now do the same for 12-degree twilight */
  if( twi->twi_to_twi<24. )
  {
    hatwilight = astronomy->ha_alt(decsun,observatory->latitude,-12.);
    if(hatwilight < -900.)
      twi->twi_to_twi12 = 24.;
    else if(hatwilight > 900.)
      twi->twi_to_twi12 = 0.;
    else
      *twi = observatory->evening_morning_twilights(-12.0, hatwilight, rasun, JDmid, observatory);
  }

  // destroy the Sun
  delete sun;
  // Forget astronomy
  delete astronomy;

}
//------------------------------------------------------------------------------
//  Computes evening and morning twilights for given altiude of Sun below horizon
Twilights Observatory::evening_morning_twilights(double alt, double hatwilight,
					    double rasun, double JDmid, Observatory *observatory)
{

  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();
  // Creates the Sun
  Sun *sun = new Sun();

  double jdtwilight;
  double stmid = astronomy->lst( JDmid, observatory->longitude);
  Twilights twi;

  // computes evening twilight
  jdtwilight = JDmid + astronomy->adj_time(rasun+hatwilight-stmid)/24.;  /* rough */
  jdtwilight = sun->jd_sun_alt(alt,jdtwilight,observatory->latitude,observatory->longitude);  /* accurate */
  if(alt==-18.0)
  {
    twi.jdetw = jdtwilight;
  }
  else if(alt==-12.0)
  {
    twi.jdetw12 = jdtwilight;
  }

  // Now do morning twilight
  jdtwilight = JDmid + astronomy->adj_time(rasun-hatwilight-stmid)/24.;
  jdtwilight = sun->jd_sun_alt(alt,jdtwilight,observatory->latitude,observatory->longitude);
  if(alt==-18.0)
  {
    twi.jdmtw = jdtwilight;
    if((twi.jdetw > 0.) && (twi.jdmtw > 0.)) twi.twi_to_twi = 24. * (twi.jdmtw - twi.jdetw);
  }
  else if(alt==-12.0)
  {
    twi.jdmtw12 = jdtwilight;
    if((twi.jdetw12 > 0.) && (twi.jdmtw12 > 0.)) twi.twi_to_twi12 = 24. * (twi.jdmtw12 - twi.jdetw12);
  }

  // destroy the Sun
  delete sun;
  // Forget astronomy
  delete astronomy;

  return twi;

}
//------------------------------------------------------------------------------
// Print out twilights
void Observatory::print_twilights(Twilights twi, double jdb, double jde, double jdcent, Observatory *observatory)
{

  if( twi.twi_to_twi==24. )
  {
    cout << endl << "Full darkness all day (sun below -18 deg)." << endl;
  }
  else if( twi.twi_to_twi==0. )
  {
    cout << endl << "Sun higher than 18-degree twilight all night." << endl;
  }
  else
  {
    cout << "18° twilight (astronomical): " ;
    if(twi.jdetw > 0.) {
      amzer t;
      t.JD = twi.jdetw - t.zone(observatory->use_dst,observatory->stdz,twi.jdetw,jdb,jde);
      t.JD2calendar();
      cout << "Evening: " << t.print_time(1,1)  << "    " ;
    }
    else cout << "Evening twilight incorrectly computed." << endl;
    if(twi.jdmtw > 0.) {
      amzer t;
      t.JD = twi.jdmtw - t.zone(observatory->use_dst,observatory->stdz,twi.jdmtw,jdb,jde);
      t.JD2calendar();
      cout << "Morning:   " << t.print_time(1,1)  << endl ;
    }
    else cout << "Morning twilight incorrectly computed.";

    if(twi.jdetw > 0. && twi.jdmtw > 0.) {
      printf("                                    %15.5f             %15.5f\n",
	     twi.jdetw,twi.jdmtw);
      printf("Julian date of night center %15.5f\n",jdcent);
    }
  }

  if( twi.twi_to_twi<24. )
  {
    if( twi.twi_to_twi12==24. )
    {
      cout << endl << "Sun always below 12-degree twilight..." << endl;
    }
    else if( twi.twi_to_twi12==0. )
    {
      cout << endl << "Sun always above 12-degree twilight..." << endl;
    }
    else
    {
      cout << "12° twilight (nautical):     "   ;
      if(twi.jdetw12 > 0.) {
	amzer t;
	t.JD = twi.jdetw12 - t.zone(observatory->use_dst,observatory->stdz,twi.jdetw12,jdb,jde);
	t.JD2calendar();
	cout << "Evening: " << t.print_time(1,1)  << "    " ;
      }
      else cout << "Evening twilight incorrectly computed." << endl;
      if(twi.jdmtw12 > 0.) {
	amzer t;
	t.JD = twi.jdmtw12 - t.zone(observatory->use_dst,observatory->stdz,twi.jdmtw12,jdb,jde);
	t.JD2calendar();
	cout << "Morning:   " << t.print_time(1,1)  << endl ;
      }
      else cout << "Morning twilight incorrectly computed.";
    }
  }
  else
  {
    cout << "No 12° twilight (nautical):     "   ;
  }
  cout <<  endl ;

}
//------------------------------------------------------------------------------
// Print out Moon coordinates
void Observatory::print_Moon_coordinates(double georamoon, double geodecmoon,
					 double toporamoon, double topodecmoon)
{
  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();

  printf("Coordinates of Moon at 0hUT  \n");
  Astronomy::coord RAMOON, DECMOON;
  printf("Geocentric coordinates:  ");
  RAMOON = astronomy->dec_to_bab(georamoon);
  DECMOON = astronomy->dec_to_bab(geodecmoon);
  printf("%2dh%2dm%5.2fs  %3d°%2d'%5.2f\n",
	 (int)RAMOON.hh,(int)RAMOON.mm,RAMOON.ss,
	 (int)DECMOON.hh,(int)DECMOON.mm,DECMOON.ss);
  printf("Topocentric coordinates: ");
  RAMOON = astronomy->dec_to_bab(toporamoon);
  DECMOON = astronomy->dec_to_bab(topodecmoon);
  printf("%2dh%2dm%5.2fs  %3d°%2d'%5.2f\n",
	 (int)RAMOON.hh,(int)RAMOON.mm,RAMOON.ss,
	 (int)DECMOON.hh,(int)DECMOON.mm,DECMOON.ss);

  // Forget astronomy
  delete astronomy;

}
//------------------------------------------------------------------------------
// Print out un coordinates
void Observatory::print_Sun_coordinates(double rasun, double decsun,
					double topora, double topodec,
					double sundist, double x, double y, double z)
{
  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();

  cout << "Coordinates of Sun at 0hUT" << endl;
  cout << "Sun RA and dec: \t" << astronomy->print_time( rasun, 2,1);
  cout << ", \t" << astronomy->print_time( decsun, 2,1)  << endl;
  cout << "Sun RA and dec topo: \t" << astronomy->print_time( topora, 2,1);
  cout << ", \t" << astronomy->print_time( topodec, 2,1)  << endl;
  cout << "Sun distance: \t" << sundist  << " AU"  << endl;
  cout << "Sun x,y,z: \t" <<  x<< " " << y << " "   << z  << " AU"   << endl  << endl;

  // Forget astronomy
  delete astronomy;

}
//------------------------------------------------------------------------------
//
int Observatory::get_parameter_from_string(string str, string param, string *value)
{
  std::size_t found = str.find(param);
  if (found!=std::string::npos)
  {
    int i = param.length()+1;
    while( str.substr(i,1)==" " )
      i++;
    *value = str.substr(i);
    return 1;
  }
  return 0;
}
int Observatory::get_parameter_from_string(string str, string param, double *value)
{
  std::size_t found = str.find(param);
  if (found!=std::string::npos)
  {
    int i = param.length();
    *value = atof(str.substr(i).c_str());
    return 1;
  }
  return 0;
}
int Observatory::get_parameter_from_string(string str, string param, short *value)
{
  std::size_t found = str.find(param);
  if (found!=std::string::npos)
  {
    int i = param.length();
    *value = atoi(str.substr(i).c_str());
    return 1;
  }
  return 0;
}
int Observatory::get_parameter_from_string(string str, string param, int *value)
{
  std::size_t found = str.find(param);
  if (found!=std::string::npos)
  {
    int i = param.length();
    *value = atoi(str.substr(i).c_str());
    return 1;
  }
  return 0;
}
int Observatory::get_parameter_from_string(string str, string param, amzer *date)
{
  char* pEnd;
  std::size_t found = str.find(param);
  if (found!=std::string::npos)
  {
    int i = param.length();
    date->year = strtol(str.substr(i).c_str(), &pEnd,10);
    date->month = strtol (pEnd,&pEnd,10);
    date->day = strtol (pEnd,&pEnd,10);
    date->hour = strtol (pEnd,&pEnd,10);
    date->min = strtol (pEnd,&pEnd,10);
    date->second = strtod (pEnd,NULL);
    date->calendar2JD();
    return 1;
  }
  return 0;
}

//------------------------------------------------------------------------------
// Read observatory parameters from ascii file */
int Observatory::read_from_file(string filename, Observatory *observatory, amzer *date,
      double *ra, double *dec, string *equinoxe, double *min_height, double *Moon_lim )
{

  string line;
  string strval;
  double value;
  int y, m, d, h, mn;
  double s;
  double JD;
  ifstream f;
  f.open(filename.c_str(), ifstream::in);
  if (f.is_open())
  {
    int i=0;
    while(f){
	getline(f, line);
	if( line!="" )
	{
	  i++;
	  if( get_parameter_from_string(line, "site name", &strval)==1 )
	  {
	    observatory->name = strval;
	  }
	  else if( get_parameter_from_string(line, "latitude", &value)==1 )
	  {
	    observatory->latitude = value;
	  }
	  else if( get_parameter_from_string(line, "longitude", &value)==1 )
	  {
	    observatory->longitude = value;
	  }
	  else if( get_parameter_from_string(line, "elevation", &value)==1 )
	  {
	    observatory->elevsea = value;
	    observatory->elevation = value;
	  }
	  else if( get_parameter_from_string(line, "zone_name", &strval)==1 )
	  {
	    observatory->zone_name = strval;
	  }
	  else if( get_parameter_from_string(line, "zabr", &strval)==1 )
	  {
	    observatory->zabr = strval;
	  }
	  else if( get_parameter_from_string(line, "stdz", &value)==1 )
	  {
	    observatory->stdz = value;
	  }
	  else if( get_parameter_from_string(line, "use_dst", &value)==1 )
	  {
	    observatory->use_dst = value;
	  }
	  else if( get_parameter_from_string(line, "date", date)==1 )
	  {
	    date->calendar2JD();
	  }
	  else if( get_parameter_from_string(line, "ra", &value)==1 )
	  {
	    *ra = value;
	  }
	  else if( get_parameter_from_string(line, "dec", &value)==1 )
	  {
	    *dec = value;
	  }
	  else if( get_parameter_from_string(line, "equinoxe", &strval)==1 )
	  {
	    *equinoxe = strval;
	  }
	  else if( get_parameter_from_string(line, "min. height", &value)==1 )
	  {
	    *min_height = value;
	  }
	  else if( get_parameter_from_string(line, "Moon distance", &value)==1 )
	  {
	    *Moon_lim = value;
	  }
	}
    }
    f.close();
    return 1;
  }
  else
  {
    *observatory = Observatory("Default observatory");
    return 0;
  }

}
//------------------------------------------------------------------------------
