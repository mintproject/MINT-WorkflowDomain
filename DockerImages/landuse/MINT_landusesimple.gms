$TITLE ECONOMIC LAND-USE CHANGE MODEL, SIMPLE
* South Sudan agriculture and forestry land-use change model, v.1
* Kelly M. Cobourn and Greg S. Amacher, June 2018
* Department of Forest Resources & Environmental Conservation
* Virginia Tech
* Contact: kellyc13@vt.edu
* The simple land-use model allocates land of heterogeneous quality
* between one agricultural crop and timber production.

$offsymlist offsymxref
option limrow = 0;
option limcol = 0;
option nlp = CONOPT;
option solprint = off;

**************************************************************************
**                  1. DEFINE LAND QUALITY CONTINUUM                    **
**************************************************************************
*Draw land quality values for N parcels from a known distribution
*over [0,1], where 0 is lowest quality land and 1 is highest quality.

sets
i                land parcels /1*10/;

parameters
q(i)             land quality draws (iid);

option seed = 1001;
loop(i,
         q(i) = uniform(0,1);
);


**************************************************************************
**                  2. AGRICULTURAL MANAGEMENT MODEL                    **
**************************************************************************
* Agricultural yield is represented using a generalized constant
* elasticity of substitution (CES) production function of the form:
* y = alpha*(beta(labor)*xlabor^rho + beta(land)*xland^rho)^(delta/rho),
* where xlabor is labor input and xland is the land input (in this case
* land quality). The simple model includes one crop, modeled after wheat.

sets
k                inputs /labor,land/;

scalars
p                crop price /11.4/
alpha            ces scale parameter /100/
rho              ces substitution parameter /0.5/
delta            ces homogeneity parameter /0.5/
int              interest rate /0.03/

parameters
w(k)             input price /labor 10/
beta(k)          ces share parameters /labor 0.7, land 0.3/;

variables
x(k)             management decisions
yield            crop production
profit           farm profit;
positive variables x,yield;

equations
yieldeq          production function
aprofit          objective function;

yieldeq.. yield =e= alpha*(sum(k, beta(k)*x(k)**rho)**(delta/rho));
aprofit.. profit =e= p*yield - sum(k, w(k)*x(k));

model maxagrent /yieldeq,aprofit/;

parameters
lstar(i,k)       optimal management decision by parcel
arent(i)         present value agricultural rents by parcel;

* Loop to solve for optimal management and rents on each parcel
loop(i,
         x.fx('land') = q(i);
         x.l('labor') = 1;
         solve maxagrent maximizing profit using nlp;
         lstar(i,k) = x.l(k);
         arent(i) = profit.l/int;
);


**************************************************************************
**                     2. FOREST MANAGEMENT MODEL                       **
**************************************************************************
* Forest growth is represented using the estimated growth function for
* U.S. southern temperate forests from Amacher et al. (2009) of the form:
* Q(t) = exp(gamma1 + gamma2/T + gamma3/T^2. We assume that timber yield
* is constant across land of differing quality. Price and planting costs
* are from Amacher et al. (2009). The management decision is the length
* of the forest rotation.

sets
g                growth function parameters /g1*g3/;

scalars
pf               stumpage price /100/
c                planting cost /84/

parameters
gamma(g)         growth function parameters /g1 9.51, g2 20.65, g3 34.01/;

variables
T                optimal rotation length
volume           forest growth function
frent            forest rent;
positive variables T,volume;

equations
growth           production function
frenteq          objective function;

growth.. volume =e= exp(gamma('g1') - gamma('g2')/T - gamma('g3')/T**2);
frenteq.. frent =e= (pf*volume*exp(-1*int*T) - c)/(1-exp(-1*int*T));

model maxfrent /growth,frenteq/;

T.lo = 1e-2;
solve maxfrent maximizing frent using nlp;


**************************************************************************
**                          3. LAND-USE MODEL                           **
**************************************************************************
* Land-use model allocates agriculture and managed forest by parcel based
* on relative rents given optimal input use (agriculture) and optimal
* rotation length (forest). Land use coded as 1 for if parcel in
* agriculture; 0 otherwise.

parameters
qcrit            critical land quality level
luse(i)          land-use prediction by parcel
prop             regional land-use proportions;

qcrit = smin(i$(arent(i) gt frent.l), q(i));
luse(i) = 1$(q(i) ge qcrit);
prop = sum(i, luse(i))/card(i);

display lstar,arent,T.l,frent.l,qcrit,luse,prop;


