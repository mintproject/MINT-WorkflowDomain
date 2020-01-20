$TITLE ETHIOPIA PMP REGIONAL MODEL OF AGRICULTURAL PRODUCTION, V.8
* Ethiopia Agricultural Production Model
* Kelly M. Cobourn and Zeya Zhang, December 2019
* Virginia Tech
* contact: kellyc13@vt.edu, zzeya7@vt.edu

$offsymlist offsymxref
option limrow = 0;
option limcol = 0;
option nlp = CONOPT;
option solprint = off;

***************************************************************************
*********************  PART 1. SETS & PARAMETERS  *************************
***************************************************************************

sets
i               crop /barley,maize,millet,pulses,sorghum,teff,wheat/
f               fertilizer supply constraint /all/
c               data type /calib,sim/
l               inputs /land,fertilizer/;
alias (i,j);

********** CALIBRATION, ECONOMIC, AND CYCLES INPUT DATA FILES *************
* Calibration of the agroeconomic model requires observed data on land area
* by crop, levels of fertilizer use by crop, crop yields, and the
* responsiveness of crop growth to additional fertilizer applications (the
* yield elasticity). 

* Basic model is agnostic to the spatial resolution of the input data. Input
* data may be specified at any aggregate level (from woreda to country) for
* which sufficient data exist. Similarly, model is agnostic to choice of year
* and can be run for any year in which input data are available.

* Required input data:
*   - Land area by crop in hectares
*   - Fertilizer applications in kilograms/hectare
*   - Crop yield in kilograms/hectare
*   - Crop prices in USD/kilogram
*   - Supply elasticities by crop (percent change in quantity supplied with
*     a percent change in price received by farmers) which are unitless
*   - Variable costs of production per unit land area in USD/hectare
*   - Variable costs of production per unit nitrogen fertilizer in USD/kilogram

table landarea(i,c) observed land allocation
$ondelim
$include landdata.csv
$offdelim
;

table cropyield(i,c) observed crop yield
$ondelim
$include yielddata.csv
$offdelim
;

table cropprice(i,c) price data
$ondelim
$include pricedata.csv
$offdelim
;

table lvarcost(i,c) variable cost data
$ondelim
$include lvardata.csv
$offdelim
;

table fvarcost(i,c) fertilizer cost data
$ondelim
$include fvardata.csv
$offdelim
;

table fertuse(i,c) observed fertilizer applications
$ondelim
$include fertdata.csv
$offdelim
;

table fertelasticity(i,c) crop nitrogen fertilizer elasticity from CYCLES
$ondelim
$include cyclesdata.csv
$offdelim
;

table supplyelasticity(i,c) supply elasticities
$ondelim
$include etadata.csv
$offdelim
;

scalars
b1              agricultural land base;
        
parameters
xbar1(i)        land area for calibration
crop(i)         crop indicator
xbar2(i)        fertilizer use for calibration
ybar(i)         crop yield for calibration
ybarN(i)        crop fertilizer yield elasticity for calibration
price(i)        crop prices
c1(i)           variable costs of production per unit land area
c2(i)           fertilizer costs     
qbar(i)         production for calibration
b(i)            land relative to total production value
eta(i)          supply elasticities;
xbar1(i) = sum(c, landarea(i,c));
crop(i)$(xbar1(i) gt 0) = 1;
xbar2(i) = sum(c, fertuse(i,c))*xbar1(i);
ybar(i) = sum(c, cropyield(i,c));
ybarN(i) = sum(c, fertelasticity(i,c));
price(i) = sum(c, cropprice(i,c));
c1(i) = sum(c, lvarcost(i,c));
c2(i) = sum(c, fvarcost(i,c));
b1 = sum(i, xbar1(i));
qbar(i) = xbar1(i)*ybar(i);
b(i)$crop(i) = sqr(xbar1(i))/(price(i)*qbar(i));
eta(i) = sum(c, supplyelasticity(i,c));


***************************************************************************
**************  PART 2. PRODUCTION FUNCTION CALIBRATION  ******************
***************************************************************************

* Set elasticities of substitution between land and nitrogen fertilizer for
* each crop.
parameters
sigma(i)        substitution elasticity by crop and technology
rho(i)          production function elasticity parameter;
sigma(i) = 0.5;
rho(i) = (sigma(i) - 1)/sigma(i);

* Ensure that calibration criteria are satisfied. The first criterion requires
* that cc1 > 0 for all i. The second criterion requires that cc2 < 0 for all i.
* A flagged value of 1 indicates failure to meet a calibration criterion.
parameters
cc1(i)          calibration criteria 1
flag1(i)        flag violations of cc1
psi(i)          term inside cc2
cc2(i)          calibration criteria 2
flag2(i)        flag violations of cc2;
cc1(i) = eta(i) - ybarN(i)/(1 - ybarN(i));
flag1(i) = 1$(cc1(i) lt 0);
psi(i) = sigma(i)*ybarN(i)/(eta(i)*(1 - ybarN(i)));
cc2(i)$crop(i) = b(i)*eta(i)*(1 - psi(i)) - sum(j$((ord(j) ne ord(i))),
         b(j)*eta(j)*sqr(1 + (1/eta(j)))*(1 + psi(j)
         - ybarN(j)));
flag2(i) = 1$(cc2(i) gt 0);

scalars
toler           tolerance for convergence /0.001/
term            indicator equal to number of crops when all deltas converge;
term = 0;

parameters          
delta0(i)       myopic CES production function parameter
adj(i)          adjustment term using myopic delta
error(i)        absolute value of change in delta
converge(i)     indicator equal to one when delta converges;
delta0(i) = eta(i)/(1 + eta(i));
adj(i)$crop(i) = 1 - (b(i)/(delta0(i)*(1-delta0(i))))/(sum(j,
         (b(j)/(delta0(j)*(1-delta0(j)))) +
         (sigma(j)*b(j)*ybarN(j)/(delta0(j)*(delta0(j)
         - ybarN(j))))));

variables
delta(i)        production function homogeneity parameters
dummy           dummy objective;
positive variables delta;

equations
etacal(i)       calibration to exogenous supply elasticity
edummy          dummy objective function;
etacal(i)$crop(i).. eta(i) =e= (delta(i)/(1-delta(i)))*adj(i);
edummy.. dummy =e= 0;

** Solve supply elasticity system of equations.
model selast /etacal,edummy/;

while(term lt card(i),
solve selast maximizing dummy using nlp;
*Test for convergence in the deltas
    error(i)$crop(i) = abs(delta0(i) - delta.l(i));
    converge(i)$(error(i) lt toler) = 1;
    term = sum(i, converge(i));        
*Update values for delta in the adjustment term if convergence test fails
    delta0(i)$crop(i)= delta.l(i);
    adj(i)$crop(i) = 1 - (b(i)/(delta0(i)*(1-delta0(i))))/(sum(j$crop(j),
            (b(j)/(delta0(j)*(1-delta0(j)))) +
            (sigma(j)*b(j)*ybarN(j)/(delta0(j)*(delta0(j)
            - ybarN(j))))));
);

variables
beta(i,l)       production function share parameters;
positive variables beta;

equations
nresp(i)        calibration against agronomic yield response to N
betas(i)        summation constraint for share parameters;
nresp(i)$crop(i).. ybarN(i)*((beta(i,'land')*(xbar1(i)**rho(i))) +
           (beta(i,'fertilizer')*(xbar2(i)**rho(i)))) =e=
           delta.l(i)*beta(i,'fertilizer')*(xbar2(i)**rho(i));
betas(i)$crop(i).. sum(l, beta(i,l)) =e= 1;

** Solve system of equations for share parameters.
model nelast /nresp,betas,edummy/;
solve nelast maximizing dummy using nlp;

parameters
mu(i)           scale parameters
lbar1           initial shadow value of land
lambda(i,l)     calibrated factor shadow values;
mu(i)$crop(i) = qbar(i)/((beta.l(i,'land')*(xbar1(i)**rho(i))) +
          (beta.l(i,'fertilizer')*xbar2(i)**rho(i)))**(delta.l(i)/rho(i));
lbar1 = sum(i$crop(i), (price(i)*qbar(i)*(delta.l(i) - ybarN(i))
        - c1(i)*xbar1(i))*xbar1(i))/sum(i$crop(i), sqr(xbar1(i)));
lambda(i,'land')$crop(i) = price(i)*qbar(i)*(delta.l(i) - ybarN(i))/xbar1(i)
             - (c1(i) + lbar1);
lambda(i,'fertilizer')$crop(i) = price(i)*qbar(i)*ybarN(i)/xbar2(i)
             - c2(i);

** Check that calibrated model reproduces observed land allocation, fertilizer
** applications, and production.
parameters
soccost(i,l)    calibrated social cost of inputs;
soccost(i,'land')$crop(i) = c1(i) + lbar1 + lambda(i,'land');
soccost(i,'fertilizer')$crop(i) = c2(i) + lambda(i,'fertilizer');

variables
x(i,l)          simulated input use
q(i)            simulated production
qprofit(i)      quasi-profit function
tprofit         total profit;
positive variables x,q,qprofit;

equations
production(i)   production function
quasiprofit(i)  quasi-profit function
obj             objective function
resconl         land constraint
resconf         fertilizer constraint;
production(i)$crop(i).. q(i) =e= mu(i)*(sum(l, beta.l(i,l)*x(i,l)**rho(i)))**(delta.l(i)/rho(i));
quasiprofit(i)$crop(i).. qprofit(i) =e= price(i)*q(i) - sum(l, soccost(i,l)*x(i,l));
obj.. tprofit =e= sum(i$crop(i), qprofit(i));
resconl.. sum(i$crop(i), x(i,'land')) =l= b1;
resconf.. sum(i$crop(i), x(i,'fertilizer')) =l= sum(i$crop(i), xbar2(i));

x.lo(i,l)$crop(i) = 0.001;

model profitmax /production,quasiprofit,obj,resconl,resconf/;
solve profitmax maximizing tprofit using nlp;

parameter
cfert(i)        simulated fertilizer applications per unit land area (kg per ha)
obsfert(i)      observed fertilizer applications (kg per ha)
clanderror(i)   deviation between simulated and observed land allocation 
cferterror(i)   deviation between simulated and observed fertilizer use 
cproderror(i)   deviation between simulated and observed production;
cfert(i)$crop(i) = x.l(i,'fertilizer')/x.l(i,'land');
obsfert(i)$crop(i) = xbar2(i)/xbar1(i);
clanderror(i) = x.l(i,'land') - xbar1(i);
cferterror(i) = cfert(i) - obsfert(i);
cproderror(i) = q.l(i) - qbar(i);

file MINT_econ_calibration /MINT_econ_calibration.txt/;
MINT_econ_calibration.pc = 5;
put MINT_econ_calibration;
put 'crop',
    'flag if cc1 violated', 'flag if cc2 violated',
    'model error land area',
    'model error fertilizer use',
    'model error crop production'/;       
loop(i$crop(i),
put i.tl,
    flag1(i), flag2(i),
    clanderror(i),
    cferterror(i),
    cproderror(i)/
);

***************************************************************************
****************  PART 3. CROP PRODUCTION SIMULATION  *********************
***************************************************************************

** Update price and production cost parameters for simulation
table pricechange(i,c) simulated change in price as a percentage
$ondelim
$include simpricedata.csv
$offdelim
;

table fertsubsidy(i,c) simulated fertilizer subsidy
$ondelim
$include simfertsubsidy.csv
$offdelim
;

table fertcon(f,c) simulated fertilizer constraint
$ondelim
$include simfertcon.csv
$offdelim
;

parameters
simprice(i)     simulated crop prices
simsoccost(i,l) simulated input costs
simfcon         simulated fertilizer constraint;
simprice(i)$crop(i) = price(i)*(1 + sum(c, pricechange(i,c)/100));
simsoccost(i,'land')$crop(i) = soccost(i,'land');
simsoccost(i,'fertilizer')$crop(i) = c2(i)*(1 + sum(c, fertsubsidy(i,c)/100)) + lambda(i,'fertilizer');
simfcon = sum(i$crop(i), xbar2(i))*(1 + sum((f,c), fertcon(f,c)/100));

** Solve simulation problem
variables
simx(i,l)       simulated input use
simq(i)         simulated production
simqprofit(i)   quasi-profit function
simtprofit      total profit;
positive variables simx,simq,simqprofit;

equations
simproduction(i) production function
simquasiprofit(i)    quasi-profit function
simobj           objective function
simresconl       land constraint
simresconf       fertilizer constraint;
simproduction(i)$crop(i).. simq(i) =e= mu(i)*(sum(l, beta.l(i,l)*simx(i,l)**rho(i)))**(delta.l(i)/rho(i));
simquasiprofit(i)$crop(i).. simqprofit(i) =e= simprice(i)*simq(i) - sum(l, simsoccost(i,l)*simx(i,l));
simobj.. simtprofit =e= sum(i$crop(i), simqprofit(i));
simresconl.. sum(i$crop(i), simx(i,'land')) =l= b1;
simresconf.. sum(i$crop(i), simx(i,'fertilizer')) =l= simfcon;

simx.lo(i,l)$crop(i) = 0.001;

model simprofitmax /simproduction,simquasiprofit,simobj,simresconl,simresconf/;
solve simprofitmax maximizing simtprofit using nlp;

** Generate and report post-optimal parameters
parameters
simcropland(i)  simulated land area by crop (1000 ha)
changeplant(i)  change in land planted by crop (%)
simagland       simulated total agricultural land (1000 ha)
changeagland    change in total agricultural land (%)
simfert(i)      simulated fertilizer applications by crop (kg per ha)
changefert(i)   change in fertilizer applications by crop (%)
simprod(i)      simulated production by crop (million kg)
changeq(i)      change in production by crop (%)
obsnetrev       observed net revenue (million USD)
simnetrev       simulated net revenue (million USD)
changenetrev    change in net revenue (%);
simcropland(i)$crop(i) = simx.l(i,'land')/1000;
changeplant(i)$crop(i) = 100*(simx.l(i,'land') - x.l(i,'land'))/x.l(i,'land');
simagland = sum(i$crop(i), simx.l(i,'land'))/1000;
changeagland = 100*((b1/1000) - simagland)/(b1/1000);
simfert(i)$crop(i) = simx.l(i,'fertilizer')/simx.l(i,'land');
changefert(i)$crop(i) = 100*(simfert(i) - obsfert(i))/obsfert(i);
simprod(i)$crop(i) = simq.l(i)/1000000;
changeq(i)$crop(i) = 100*(simq.l(i) - q.l(i))/q.l(i);
obsnetrev = sum(i$crop(i), price(i)*q.l(i) - c1(i)*x.l(i,'land') - c2(i)*x.l(i,'fertilizer'))/1000000;
simnetrev = sum(i$crop(i), simprice(i)*simq.l(i) - c1(i)*simx.l(i,'land') -
            c2(i)*(1 + sum(c, fertsubsidy(i,c)/100))*simx.l(i,'fertilizer'))/1000000;
changenetrev = 100*(simnetrev - obsnetrev)/obsnetrev;

file MINT_econ_simout /MINT_econ_simulation.txt/;
MINT_econ_simout.pc = 5;
put MINT_econ_simout;
put 'crop',
    'sim crop land (k ha)', 'change crop land (%)',
    'sim ag land (k ha)', 'change ag land (%)',
    'sim fert rate (kg/ha)', 'change fert rate (%)',
    'sim production (m kg)', 'change production (%)',
    'sim net revenue (m USD)', 'change net revenue (%)'/;         
loop(i$crop(i),
put i.tl,
    simcropland(i), changeplant(i),
    simagland, changeagland,
    simfert(i), changefert(i),
    simprod(i), changeq(i),
    simnetrev, changenetrev/
);