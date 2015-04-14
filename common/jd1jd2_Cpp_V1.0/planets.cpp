#include "planets.h"

//------------------------------------------------------------------------------
// Constructor
Planets::Planets()
{
}
//------------------------------------------------------------------------------
// Destructor
Planets::~Planets()
{
}

//------------------------------------------------------------------------------
// computes and loads mean elements for planets.
void Planets::comp_el( double jd)
{

   jd_el = jd;   // true, but not necessarily; set explicitly
   double d = jd - 2415020.;
   double T = d / 36525.;
   double Tsq = T * T;
   double Tcb = Tsq * T;

   // Mercury, Venus, and Mars from Explanatory Suppl., p. 113

   el[1].name = "Mercury";
   el[1].incl = 7.002880 + 1.8608e-3 * T - 1.83e-5 * Tsq;
   el[1].Omega = 47.14594 + 1.185208 * T + 1.74e-4 * Tsq;
   el[1].omega = 75.899697 + 1.55549 * T + 2.95e-4 * Tsq;
   el[1].a = .3870986;
   el[1].daily = 4.0923388;
   el[1].ecc = 0.20561421 + 0.00002046 * T;
   el[1].L_0 = 178.179078 + 4.0923770233 * d  +
    0.0000226 * pow((3.6525 * T),2.);

   el[2].name = "Venus  ";
   el[2].incl = 3.39363 + 1.00583e-03 * T - 9.722e-7 * Tsq;
   el[2].Omega = 75.7796472 + 0.89985 * T + 4.1e-4 * Tsq;
   el[2].omega = 130.16383 + 1.4080 * T + 9.764e-4 * Tsq;
   el[2].a = .723325;
   el[2].daily = 1.60213049;
   el[2].ecc = 0.00682069 - 0.00004774 * T;
   el[2].L_0 = 342.767053 + 1.6021687039 * 36525 * T +
    0.000023212 * pow((3.6525 * T),2.);

   // Earth from old Nautical Almanac ....

   el[3].name = "Earth  ";
   el[3].ecc = 0.01675104 - 0.00004180*T + 0.000000126*Tsq;
   el[3].incl = 0.0;
   el[3].Omega = 0.0;
   el[3].omega = 101.22083 + 0.0000470684*d + 0.000453*Tsq + 0.000003*Tcb;
   el[3].a = 1.0000007;;
   el[3].daily = 0.985599;
   el[3].L_0 = 358.47583 + 0.9856002670*d - 0.000150*Tsq - 0.000003*Tcb +
       el[3].omega;

   el[4].name = "Mars   ";
   el[4].incl = 1.85033 - 6.75e-04 * T - 1.833e-5 * Tsq;
   el[4].Omega = 48.786442 + .770992 * T + 1.39e-6 * Tsq;
   el[4].omega = 334.218203 + 1.840758 * T + 1.299e-4 * Tsq;
   el[4].a = 1.5236915;
   el[4].daily = 0.5240329502 + 1.285e-9 * T;
   el[4].ecc = 0.09331290 - 0.000092064 * T - 0.000000077 * Tsq;
   el[4].L_0 = 293.747628 + 0.5240711638 * d  +
    0.000023287 * pow((3.6525 * T),2.);

   // Outer planets from Jean Meeus, Astronomical Formulae for
   //   Calculators, 3rd edition, Willman-Bell; p. 100.

   el[5].name = "Jupiter";
   el[5].incl = 1.308736 - 0.0056961 * T + 0.0000039 * Tsq;
   el[5].Omega = 99.443414 + 1.0105300 * T + 0.0003522 * Tsq
      - 0.00000851 * Tcb;
   el[5].omega = 12.720972 + 1.6099617 * T + 1.05627e-3 * Tsq
   - 3.43e-6 * Tcb;
   el[5].a = 5.202561;
   el[5].daily = 0.08312941782;
   el[5].ecc = .04833475  + 1.64180e-4 * T - 4.676e-7*Tsq -
   1.7e-9 * Tcb;
   el[5].L_0 = 238.049257 + 3036.301986 * T + 0.0003347 * Tsq -
   1.65e-6 * Tcb;

   // The outer planets have such large mutual interactions that
   //   even fair accuracy requires lots of perturbations --- here
   //   are some of the larger ones, from Meeus' book.

   double ups = 0.2*T + 0.1;
   double P = (237.47555 + 3034.9061 * T) / DEG_IN_RADIAN;
   double Q = (265.91650 + 1222.1139 * T) / DEG_IN_RADIAN;
   double S = (243.51721 + 428.4677 * T) / DEG_IN_RADIAN;
   double V = 5*Q - 2*P;
   double W = 2*P - 6*Q + 3*S;
   double zeta = Q - P;
//   double psi = S - Q;
   double sinQ = sin(Q);
   double cosQ = cos(Q);
   double sinV = sin(V);
   double cosV = cos(V);
   double sinZeta = sin(zeta);
   double cosZeta = cos(zeta);
   double sin2Zeta = sin(2*zeta);
   double cos2Zeta = cos(2*zeta);

   el[5].L_0 = el[5].L_0
   + (0.331364 - 0.010281*ups - 0.004692*ups*ups)*sinV
   + (0.003228 - 0.064436*ups + 0.002075*ups*ups)*cosV
   - (0.003083 + 0.000275*ups - 0.000489*ups*ups)*sin(2*V)
   + 0.002472 * sin(W) + 0.013619 * sinZeta + 0.018472 * sin2Zeta
   + 0.006717 * sin(3*zeta)
   + (0.007275  - 0.001253*ups) * sinZeta * sinQ
   + 0.006417 * sin2Zeta * sinQ
   - (0.033839 + 0.001253 * ups) * cosZeta * sinQ
   - (0.035681 + 0.001208 * ups) * sinZeta * sinQ;
   // only part of the terms, the ones first on the list and
   //   selected larger-amplitude terms from farther down.

   el[5].ecc = el[5].ecc + 1e-7 * (
     (3606 + 130 * ups - 43 * ups*ups) * sinV
   + (1289 - 580 * ups) * cosV - 6764 * sinZeta * sinQ
   - 1110 * sin2Zeta * sin(Q)
   + (1284 + 116 * ups) * cosZeta * sinQ
   + (1460 + 130 * ups) * sinZeta * cosQ
   + 6074 * cosZeta * cosQ);

   el[5].omega = el[5].omega
   + (0.007192 - 0.003147 * ups) * sinV
   + ( 0.000197*ups*ups - 0.00675*ups - 0.020428) * cosV
   + 0.034036 * cosZeta * sinQ + 0.037761 * sinZeta * cosQ;

   el[5].a = el[5].a + 1.0e-6 * (
   205 * cosZeta - 263 * cosV + 693 * cos2Zeta + 312 * sin(3*zeta)
   + 147 * cos(4*zeta) + 299 * sinZeta * sinQ
   + 181 * cos2Zeta * sinQ + 181 * cos2Zeta * sinQ
   + 204 * sin2Zeta * cosQ + 111 * sin(3*zeta) * cosQ
   - 337 * cosZeta * cosQ - 111 * cos2Zeta * cosQ
   );

   el[6].name = "Saturn ";
   el[6].incl = 2.492519 - 0.00034550*T - 7.28e-7*Tsq;
   el[6].Omega = 112.790414 + 0.8731951*T - 0.00015218*Tsq - 5.31e-6*Tcb ;
   el[6].omega = 91.098214 + 1.9584158*T + 8.2636e-4*Tsq;
   el[6].a = 9.554747;
   el[6].daily = 0.0334978749897;
   el[6].ecc = 0.05589232 - 3.4550e-4 * T - 7.28e-7*Tsq;
   el[6].L_0 = 266.564377 + 1223.509884*T + 0.0003245*Tsq - 5.8e-6*Tcb
   + (0.018150*ups - 0.814181 + 0.016714 * ups*ups) * sinV
   + (0.160906*ups - 0.010497 - 0.004100 * ups*ups) * cosV
   + 0.007581 * sin(2*V) - 0.007986 * sin(W)
   - 0.148811 * sinZeta - 0.040786*sin2Zeta
   - 0.015208 * sin(3*zeta) - 0.006339 * sin(4*zeta)
   - 0.006244 * sinQ
   + (0.008931 + 0.002728 * ups) * sinZeta * sinQ
   - 0.016500 * sin2Zeta * sinQ
   - 0.005775 * sin(3*zeta) * sinQ
   + (0.081344 + 0.003206 * ups) * cosZeta * sinQ
   + 0.015019 * cos2Zeta * sinQ
   + (0.085581 + 0.002494 * ups) * sinZeta * cosQ
   + (0.025328 - 0.003117 * ups) * cosZeta * cosQ
   + 0.014394 * cos2Zeta * cosQ;  // truncated here -- no terms larger than 0.01
                                  // degrees, but errors may accumulate beyond this
   el[6].ecc = el[6].ecc + 1.0e-7 * (
     (2458 * ups - 7927.) * sinV + (13381. + 1226. * ups) * cosV
   + 12415. * sinQ + 26599. * cosZeta * sinQ
   - 4687. * cos2Zeta * sinQ - 12696. * sinZeta * cosQ
   - 4200. * sin2Zeta * cosQ +(2211. - 286*ups) * sinZeta*sin(2*Q)
   - 2208. * sin2Zeta * sin(2*Q)
   - 2780. * cosZeta * sin(2*Q) + 2022. * cos2Zeta*sin(2*Q)
   - 2842. * sinZeta * cos(2*Q) - 1594. * cosZeta * cos(2*Q)
   + 2162. * cos2Zeta*cos(2*Q) ); // terms with amplitudes > 2000e-7;
                                  // some secular variation ignored.
   el[6].omega = el[6].omega
   + (0.077108 + 0.007186 * ups - 0.001533 * ups*ups) * sinV
   + (0.045803 - 0.014766 * ups - 0.000536 * ups*ups) * cosV
   - 0.075825 * sinZeta * sinQ - 0.024839 * sin2Zeta*sinQ
   - 0.072582 * cosQ - 0.150383 * cosZeta * cosQ +
   0.026897 * cos2Zeta * cosQ;    // all terms with amplitudes greater than 0.02
                                  // degrees -- lots of others!
   el[6].a = el[6].a + 1.0e-6 * (
   2933. * cosV + 33629. * cosZeta - 3081. * cos2Zeta
   - 1423. * cos(3*zeta) + 1098. * sinQ - 2812. * sinZeta * sinQ
   + 2138. * cosZeta * sinQ  + 2206. * sinZeta * cosQ
   - 1590. * sin2Zeta*cosQ + 2885. * cosZeta * cosQ
   + 2172. * cos2Zeta * cosQ);  // terms with amplitudes greater than 1000 x 1e-6

   el[7].name = "Uranus ";
   el[7].incl = 0.772464 + 0.0006253*T + 0.0000395*Tsq;
   el[7].Omega = 73.477111 + 0.4986678*T + 0.0013117*Tsq;
   el[7].omega = 171.548692 + 1.4844328*T + 2.37e-4*Tsq - 6.1e-7*Tcb;
   el[7].a = 19.21814;
   el[7].daily = 1.1769022484e-2;
   el[7].ecc = 0.0463444 - 2.658e-5 * T;
   el[7].L_0 = 244.197470 + 429.863546*T + 0.000316*Tsq - 6e-7*Tcb;
   // stick in a little bit of perturbation -- this one really gets
   //   yanked around.... after Meeus p. 116
   double G = (83.76922 + 218.4901 * T)/DEG_IN_RADIAN;
   double H = 2*G - S;
   el[7].L_0 = el[7].L_0 + (0.864319 - 0.001583 * ups) * sin(H)
   + (0.082222 - 0.006833 * ups) * cos(H)
   + 0.036017 * sin(2*H);
   el[7].omega = el[7].omega + 0.120303 * sin(H)
   + (0.019472 - 0.000947 * ups) * cos(H)
   + 0.006197 * sin(2*H);
   el[7].ecc = el[7].ecc + 1.0e-7 * (
   20981. * cos(H) - 3349. * sin(H) + 1311. * cos(2*H));
   el[7].a = el[7].a - 0.003825 * cos(H);

   // other corrections to "true longitude" are ignored.

   el[8].name = "Neptune";
   el[8].incl = 1.779242 - 9.5436e-3 * T - 9.1e-6*Tsq;
   el[8].Omega = 130.681389 + 1.0989350 * T + 2.4987e-4*Tsq - 4.718e-6*Tcb;
   el[8].omega = 46.727364 + 1.4245744*T + 3.9082e-3*Tsq - 6.05e-7*Tcb;
   el[8].a = 30.10957;
   el[8].daily = 6.020148227e-3;
   el[8].ecc = 0.00899704 + 6.33e-6 * T;
   el[8].L_0 = 84.457994 + 219.885914*T + 0.0003205*Tsq - 6e-7*Tcb;
   el[8].L_0 = el[8].L_0
   - (0.589833 - 0.001089 * ups) * sin(H)
   - (0.056094 - 0.004658 * ups) * cos(H)
   - 0.024286 * sin(2*H);
   el[8].omega = el[8].omega + 0.024039 * sin(H)
   - 0.025303 * cos(H);
   el[8].ecc = el[8].ecc + 1.0e-7 * (
   4389. * sin(H) + 1129. * sin(2.*H)
   + 4262. * cos(H) + 1089. * cos(2.*H));
   el[8].a = el[8].a + 8.189e-3 * cos(H);

// crummy -- osculating elements a la Sept 15 1992

   d = jd - 2448880.5;  // 1992 Sep 15
   T = d / 36525.;
   el[9].name = "Pluto  ";
   el[9].incl = 17.1426;
   el[9].Omega = 110.180;
   el[9].omega = 223.782;
   el[9].a = 39.7465;
   el[9].daily = 0.00393329;
   el[9].ecc = 0.253834;
   el[9].L_0 = 228.1027 + 0.00393329 * d;

   el[1].mass = 1.660137e-7;  // in units of sun's mass, IAU 1976
   el[2].mass = 2.447840e-6;  // from 1992 *Astron Almanac*, p. K7
   el[3].mass = 3.040433e-6;  // earth + moon
   el[4].mass = 3.227149e-7;
   el[5].mass = 9.547907e-4;
   el[6].mass = 2.858776e-4;
   el[7].mass = 4.355401e-5;
   el[8].mass = 5.177591e-5;
   el[9].mass = 7.69e-9;  // Pluto+Charon -- ?

}
//------------------------------------------------------------------------------
// produces ecliptic x,y,z coordinates for planet number 'p' at date jd.
// see 1992 Astronomical Almanac, p. E 4 for these formulae.
void Planets::planetxyz( int p, double jd, double *x, double *y, double *z)
{
   double ii = el[p].incl/DEG_IN_RADIAN;
   double e = el[p].ecc;

   double LL = (el[p].daily * (jd - jd_el) + el[p].L_0) / DEG_IN_RADIAN;
   double Om = el[p].Omega / DEG_IN_RADIAN;
   double om = el[p].omega / DEG_IN_RADIAN;

   double M = LL - om;
   double omnotil = om - Om;
   double nu = M + (2.*e - 0.25 * pow(e,3.)) * sin(M) +
        1.25 * e * e * sin(2 * M) +
        1.08333333 * pow(e,3.) * sin(3 * M);
   double r = el[p].a * (1. - e*e) / (1 + e * cos(nu));

   *x = r * (cos(nu + omnotil) * cos(Om) - sin(nu +  omnotil) * cos(ii) * sin(Om));
   *y = r * (cos(nu + omnotil) * sin(Om) + sin(nu +  omnotil) * cos(ii) * cos(Om));
   *z = r *  sin(nu + omnotil) * sin(ii);
}
//------------------------------------------------------------------------------
// numerically evaluates planet velocity by brute-force
// numerical differentiation. Very unsophisticated algorithm.
void Planets::planetvel( int p, double jd, double *vx, double *vy, double *vz)
{
   double x1,y1,z1,x2,y2,z2;
   double dt = 0.1 / el[p].daily; // timestep: time for mean motion of 0.1 degree */
   planetxyz(p, (jd - dt), &x1, &y1, &z1);
   planetxyz(p, (jd + dt), &x2, &y2, &z2);
   *vx = 0.5 * (x2 - x1) / dt;
   *vy = 0.5 * (y2 - y1) / dt;
   *vz = 0.5 * (z2 - z1) / dt;
}
//------------------------------------------------------------------------------
// simply transforms a vector x, y, and z to 2000 coordinates and prints
// for use in diagnostics. answer should be in ecliptic coordinates, in AU per day.
string Planets::xyz2000( double jd ,double *x, double *y, double *z)
{
   Astronomy *astro = new Astronomy;
   ostringstream oss;
   string str;
   double r1, d1, ep1, r2, d2;
   double mod = sqrt(*x * *x + *y * *y + *z * *z);
   astro->xyz_cel(*x,*y,*z,&r1,&d1);
   ep1 = 2000. + (jd - J2000)/365.25;
   astro->precess(r1,d1,2000.,ep1,&r2,&d2,XFORM_JUSTPRE,XFORM_TOSTDEP);
   *x = mod * cos(r2/HRS_IN_RADIAN) * cos(d2/DEG_IN_RADIAN);
   *y = mod * sin(r2/HRS_IN_RADIAN) * cos(d2/DEG_IN_RADIAN);
   *z = mod * sin(d2/DEG_IN_RADIAN);
   oss << ep1 << " to 2000 --> " << x << " " << y << " " << z ;
   str=oss.str();
   delete astro;
   return str;
}
//------------------------------------------------------------------------------
// simply transforms a vector x, y, and z to 2000 coordinates
//   and hands it back through pointers.  For really transforming it!
void Planets::xyz2000xf( double jd, double *x, double *y, double *z)
{
   Astronomy *astro = new Astronomy;
   double r1, d1, r2, d2;
   double mod = sqrt( *x * *x + *y * *y + *z * *z );
   astro->xyz_cel(*x,*y,*z,&r1,&d1);
   double ep1 = 2000. + (jd - J2000)/365.25;
   astro->precess(r1,d1,2000.,ep1,&r2,&d2,XFORM_JUSTPRE,XFORM_TOSTDEP);
   *x = mod * cos(r2/HRS_IN_RADIAN) * cos(d2/DEG_IN_RADIAN);
   *y = mod * sin(r2/HRS_IN_RADIAN) * cos(d2/DEG_IN_RADIAN);
   *z = mod * sin(d2/DEG_IN_RADIAN);
   delete astro;
}
//------------------------------------------------------------------------------
// Computes ra and dec of i-th planet as viewed from earth.
// given computed planet positions for planets 1-10, computes
// ra and dec of i-th planet as viewed from earth (3rd).
void Planets::earthview( double *x, double *y, double *z, int i, double *ra, double *dec)
{
   Astronomy *astro = new Astronomy;
   double dx = x[i] - x[3];
   double dy = y[i] - y[3];
   double dz = z[i] - z[3];
   astro->xyz_cel(dx,dy,dz,ra,dec);
   delete astro;
}
//------------------------------------------------------------------------------
