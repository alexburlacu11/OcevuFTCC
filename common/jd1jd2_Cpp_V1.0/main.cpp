// g++ -o astro observatory.cpp amzer.cpp astronomy.cpp sun.cpp moon.cpp planets.cpp main.cpp

#include "astronomy.h"
bool verbose;
string siteName="Default observatory";
string dateStr="Default observatory";

//------------------------------------------------------------------------------
int print_help()
{
  cout << endl;
  cout << "Usage: ./astro [-h] [-f filename]" << endl;
  cout << "Usage: ./astro [-h] [-o name] [-d date] || [-j JD] [-c ra dec equinoxe -m]" << endl;
  cout << "Usage:   -h : help" << endl;
  cout << "Usage:   -v : verbose" << endl;
  cout << "Usage:   -f filename : parameter file" << endl;
  cout << "Usage:   -o  name : observatory name" << endl;
  cout << "Usage:   -d  date : calendar date (ex. 2014 6 25 19 35 45.6)" << endl;
  cout << "Usage:   -j  JD : julian date (ex. 2456834.3165)" << endl;
  cout << "Usage:   -c  ra dec equinoxe : equatorial coordiantes of object" << endl;
  cout << "Usage:   -m  minimum height of object above horizon (>0)" << endl;
  cout << "Usage:   -l  limit acceptable distance to the Moon (degrees)" << endl;
  cout << endl;
  cout << "Examples: ./astro -o \"La Silla\"" << endl;
  cout << "          ./astro -o Toulouse" << endl;
  cout << "          ./astro -f parameters.txt" << endl;
  cout << endl;
  cout << "(-o -d -j -c) and -f options are incompatible. if both are used, -f superseed -o" << endl;
  cout << "-d and -j are are 2 options for the same parameter, the date. if both are used, -j superseed -d" << endl;
  cout << endl;
}
//------------------------------------------------------------------------------
int main(int argc, char *argv[])
{
  double JD1,JD2;
  JD1=0.0;
  JD2=0.0;
  amzer date;
  double ra, dec;
  string equinoxe;
  double min_height;
  min_height=0.0;
  double Moon_lim;
  Moon_lim=50.0;
  double distmoon;

  // --------------------------------------------------------------------------
  //  test argument validity

  if ( (argc == 0) || ((argc == 2 && strcmp(argv[1], "-h")==0) ) )
  {
    print_help();
    exit(0);
  }

  // ------------------------------------------------------------------------
  // examines options
  string filename="";

  for ( int i = 1 ; i < argc ; i++ )
  {
      if ( strcmp(argv[i], "-v") == 0 )
      {
	verbose = true;
      }
      else if ( strcmp(argv[i], "-f") == 0 )
      {
	i++;
	if( i < argc ){
	  filename=argv[i];
	} else {
	  if(verbose)
	  {
	    cout << "ERROR:  no parameter file name !" << endl << endl;
	    print_help();
	  }
	  exit(1);
	}
      }
      else if ( strcmp(argv[i], "-o") == 0 )
      {
	i++;
	if( i < argc ){
	  siteName=argv[i];
	} else {
	  if(verbose)
	  {
	    cout << "ERROR:  no valid observatory name !" << endl << endl;
	    print_help();
	  }
	  exit(1);
	}
      }
      else if ( strcmp(argv[i], "-d") == 0 )
      {
	int j;
	double s;
	i++;
	sscanf(argv[i++], "%d", &j);
	date.year=j;
	sscanf(argv[i++], "%d", &j);
	date.month=j;
	sscanf(argv[i++], "%d", &j);
	date.day=j;
	sscanf(argv[i++], "%d", &j);
	date.hour=j;
	sscanf(argv[i++], "%d", &j);
	date.min=j;
	sscanf(argv[i], "%lf", &s);
	date.second=s;
	date.calendar2JD();
      }
      else if ( strcmp(argv[i], "-j") == 0 )
      {
	i++;
	double j;
	if( i < argc ){
	  if( sscanf(argv[i], "%lf", &j) != 1) {
	    if(verbose)
	    {
	      cout << "ERROR: double awaited  !" << endl << endl;
	      exit(EXIT_FAILURE);
	    }
	  }
	  date.JD=j;
	  date.JD2calendar();
	} else {
	  if(verbose)
	  {
	    cout << "ERROR:  no valid julian date !" << endl << endl;
	    print_help();
	  }
	  exit(1);
	}
      }
      else if ( strcmp(argv[i], "-m") == 0 )
      {
	i++;
	double j;
	if( i < argc ){
	  if( sscanf(argv[i], "%lf", &j) != 1) {
	    if(verbose)
	    {
	      cout << "ERROR: double awaited  !" << endl << endl;
	      exit(EXIT_FAILURE);
	    }
	  }
	  if( j>0 ) min_height=j;
	} else {
	  if(verbose)
	  {
	    cout << "ERROR:  no valid minimum height above horizon !" << endl << endl;
	    print_help();
	  }
	  exit(1);
	}
      }
      else if ( strcmp(argv[i], "-l") == 0 )
      {
	i++;
	double j;
	if( i < argc ){
	  if( sscanf(argv[i], "%lf", &j) != 1) {
	    if(verbose)
	    {
	      cout << "ERROR: double awaited  !" << endl << endl;
	      exit(EXIT_FAILURE);
	    }
	  }
	  if( j>0 ) Moon_lim=j;
	} else {
	  if(verbose)
	  {
	    cout << "ERROR:  no valid value of acceptable distance to the Moon !" << endl << endl;
	    print_help();
	  }
	  exit(1);
	}
      }
      else
      {
	if(verbose)
	{
	  cout << "ERROR:  Option not allowed !" << endl << endl;
	  print_help();
	}
	exit(1);
      }
  }

  // Creates astronomy environment
  Astronomy *astronomy = new Astronomy();

  // Creates an observatory
  Observatory *observatory = new Observatory("");
  if( filename!="" )
  {
    if(verbose) cout << endl;
    int i = observatory->read_from_file( filename, observatory, &date,
		      &ra, &dec, &equinoxe, &min_height, &Moon_lim);
    if( i==1 )
    {
      siteName = observatory->name;
    } else {
      if(verbose)
      {
	cout << "ERROR:  cannot open parameter file" << endl << endl;
	print_help();
      }
      exit(1);
    }

  } else {
    *observatory = Observatory(siteName);
  }

  if(verbose) cout << "######################################################################" << endl;
  if(verbose) cout << "Observatory: " << observatory->name << endl;
  if(verbose) cout << "geographic coordinates (latitude, longitude): " << observatory->latitude << ", "  <<  observatory->longitude << " elevation: "  <<  observatory->elevsea << " m"  <<  endl;

  double jdb, jde;
  double jd0 = date.JD;
  if(verbose)
  {
    cout << "Given date " << date.print_all(1,3)<< endl;
    printf("Given julian date %15.5f\n\n",date.JD);
  }
  // day saving time bounds for the year:
  observatory->find_dst_bounds( date.year, observatory->stdz, observatory->use_dst, &jdb, &jde);
  // Creates the Sun
  Sun *sun = new Sun();
  // Creates the Moon
  Moon *moon = new Moon();

  double jdstart,jdend; // time interval to consider if object is observable
  amzer dateMid; // Local midnight
  Twilights twi; // Twilights
  double stmid;  // Sidereal time at local midnight
  double horiz=0.0; // altitude of horizon
  double jdsunset, jdsunrise;  // Julian date of Sun set and Sun rise
  float set_to_rise; // Time interval between Sun set and Sun rise (in hours)
  double jdcent;  // Julian date of night center




  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --
  // Is jd0 in the current night ?
  // If not, consider next night

  // Julian date at local midnight
  dateMid.JD = (int) date.JD +0.5 ;  // local midnight
  dateMid.JD  = dateMid.JD + dateMid.zone(observatory->use_dst,observatory->stdz,dateMid.JD ,jdb,jde) / 24.;
  // Sidereal time at local midnight
  stmid = astronomy->lst( dateMid.JD, observatory->longitude);
  // Coordinates of the Sun
  sun->accusun(dateMid.JD,stmid,observatory->latitude, sun);
  // Computes Sun set and rise
  observatory->sunSetRise(dateMid.JD, sun->ra, sun->dec, observatory, horiz, jdb, jde,
			  &jdsunset, &jdsunrise,&set_to_rise, &jdcent);

  // Are there twilights ?
  if( set_to_rise == 0.) // No twilights
  {
    twi.twi_to_twi = 0.;
    jdstart = 0;
    jdend = 0;
  }
  else
  {
    // computes twilights
    observatory->twilights(dateMid.JD, sun->ra, sun->dec, observatory, jdb, jde, &twi);

    if( jd0>twi.jdetw && jd0<twi.jdmtw ) {
      if(verbose) cout << "Given date is in the current night" << endl << endl;
      jdstart = jd0;
      jdend = twi.jdmtw;
    } else {
      if(verbose) cout << "Given date is not during night. Consider next night" << endl << endl;

      // julian date at local midnight, next night
      dateMid.JD = (int) date.JD +1.5 ;  // local midnight next night
      dateMid.JD  = dateMid.JD + dateMid.zone(observatory->use_dst,observatory->stdz,dateMid.JD ,jdb,jde) / 24.;
      // Sidereal time at local midnight
      stmid = astronomy->lst( dateMid.JD, observatory->longitude);
      // Coordinates of the Sun
      sun->accusun(dateMid.JD,stmid,observatory->latitude, sun);
      // Computes Sun set and rise
      observatory->sunSetRise(dateMid.JD, sun->ra, sun->dec, observatory, horiz, jdb, jde,
			      &jdsunset, &jdsunrise,&set_to_rise, &jdcent);
      // computes twilights
      observatory->twilights(dateMid.JD, sun->ra, sun->dec, observatory, jdb, jde, &twi);
      jdstart = twi.jdetw;
      jdend = twi.jdmtw;

    }
    if(verbose) printf("twilights  %15.5f    %15.5f (night center %15.5f)\n",twi.jdetw,twi.jdmtw,jdcent);
    if(verbose) printf("Julian date interval to consider   %15.5f   %15.5f\n\n",jdstart,jdend);

  }




  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --
  // Is object observable ?
  if( jdstart!=0 && jdend!=0 )
  {
    // convert object coordinates from standard epoch to epoch of date
    double rout, dout;
    double std_epoch=2000.0;
    if( equinoxe=="J2000" ) std_epoch=2000.0;
    if( equinoxe=="B1950" ) std_epoch=1950.0;
    if( equinoxe=="B1900" ) std_epoch=1900.0;
    double date_epoch;
    date_epoch = 2000.0 + (jdcent-2451545.0)/365.25;
    if(verbose) cout << endl << endl;
    if(verbose) cout << "ra " << ra <<  "  dec " << dec << endl;
    if(verbose) cout << "std_epoch " << std_epoch << endl;
    if(verbose) cout << "date_epoch " << date_epoch << endl;

    astronomy->precess( ra, dec, std_epoch, date_epoch, &rout, &dout, 0, 1);
    if(verbose) cout << "raout " << rout <<  "  decout " << rout << endl;
    if(verbose) cout << endl << endl;

    // Computes rise, transit and set of the object
    double HA = astronomy->ha_alt(dout,observatory->latitude,min_height);
    double jdtransit,jdrise,jdset;
    if(HA>900.) // circum-polar object
    {
      jdtransit = dateMid.JD + astronomy->adj_time(rout-stmid)/24.0;
      jdrise = jdtransit-0.5;
      jdset = jdtransit+0.5;
    }
    else
    {
      jdrise = dateMid.JD + astronomy->adj_time(rout-HA-stmid)/24.0;
      jdset  = dateMid.JD + astronomy->adj_time(rout+HA-stmid)/24.0;
      if(jdrise>jdset) jdset = jdset+1.0;
      jdtransit = (jdset+jdrise)/2.0;
    }
    if(verbose) cout << "Minimum height above horizon " << min_height << endl;
    if(verbose) printf("jdrise   %15.5f\n",jdrise);
    if(verbose) printf("jdtransit   %15.5f\n",jdtransit);
    if(verbose) printf("jdset   %15.5f\n",jdset);
    if(verbose) cout << endl << endl;

    // Coordinates of the Moon at local midnight
    moon->accumoon( dateMid.JD, observatory->latitude, stmid, observatory->elevsea, moon);
    //  Moon distance at local midnight
    distmoon = astronomy->subtend(rout/15.0,dout,moon->topora,moon->topodec);
    distmoon = distmoon * DEG_IN_RADIAN;

    if(verbose) cout << "Acceptable distance to the Moon " << Moon_lim << endl;
    if(verbose) cout << "distance to the Moon " << distmoon << endl;

    // If not too close to the Moon, computes JD1 and JD2
    if( distmoon>Moon_lim )
    {
      if( jdstart<jdrise && jdrise<jdset && jdset< jdend )
      {
	JD1 = jdrise;
	JD2 = jdset;
      }

      if( jdrise<jdstart && jdstart<jdset && jdset<jdend )
      {
	JD1 = jdstart;
	JD2 = jdset;
      }

      if( jdstart<jdrise && jdrise<jdend && jdend<jdset )
      {
	JD1 = jdrise;
	JD2 = jdend;
      }

      if( jdrise<jdstart && jdstart<jdend && jdend<jdset )
      {
	JD1 = jdstart;
	JD2 = jdend;
      }
    }

  }

  if(verbose) cout << endl;
  if(verbose) cout << "######################################################################" << endl;
  if(verbose) cout << endl;
  printf("jd1 = %15.5f \n",JD1);
  printf("jd2 = %15.5f \n",JD2);
  printf("moon_dist = %6.1f \n",distmoon);
  if(verbose) cout << endl << endl;
  return 0;
}

//------------------------------------------------------------------------------

