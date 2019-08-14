$TITLE SOUTH SUDAN PMP MODEL OF AGRICULTURAL PRODUCTION
* South Sudan CROP SIMPLE model, v.2
* Kelly M. Cobourn, November 2018
* Department of Forest Resources and Environmental Conservation
* Virginia Tech
* email: kellyc13@vt.edu

$offsymlist offsymxref
option limrow = 0;
option limcol = 0;
option nlp = CONOPT;
option solprint = off;

***************************************************************************
*********************  PART 1. SETS & PARAMETERS  *************************
***************************************************************************

sets
i        crop /cassava,groundnuts,maize,sesame,sorghum/
l        inputs /land,fertilizer/
calib    calibration data /xbar1,xbar2,ybar/
econ     economic data /p,eta,c1,c2/
cycles   cycles outputs /ybarN/;
alias (i,j);

********** CALIBRATION, ECONOMIC, AND CYCLES INPUT DATA FILES *************
* Land use and yield information are used for the country in aggregate. Remote
* sensing data could identify the land area allocated to each crop in the Pongo
* Basin, specifically. Land use and yield information are from FAOSTAT for 2016.
* Land areas are in ha; yield is in kg/ha.
table    calibdata(i,calib) observed land allocation and yield
$ondelim
$include calibdata2016.csv
$offdelim
;

* Changes to the econ data input file support scenarios with changes in
* relative crop prices, supply elasticities, or costs of production. Crop
* prices are from FAOSTAT for 2016 in USD/kg. Supply elasticities are from
* the economic literature for similar countries or regions. Costs of production
* for land (c1) are in USD/ha; for N fertilizer (c2) in USD/kg. Inputs other
* than land and fertilizer are assumed to be used in fixed proportion to land
* and are included in c1.
table    econdata(i,econ) econ input data
$ondelim
$include econdata2016.csv
$offdelim
;

** Link with CYCLES by extracting the sensitivity of crop yield to N
** fertilizer applications at the observed level of N fertilizer use.
table  cyclesdata(i,cycles) yield elasticity with respect to N
$ondelim
$include cyclesdata2016.csv
$offdelim
;

display calibdata, econdata, cyclesdata;

scalar
b1       agricultural land base;
b1 = sum(i, calibdata(i,'xbar1'));

parameters
qbar(i)  reference crop production
b(i)     land relative to total production value;
qbar(i) = calibdata(i,'xbar1')*calibdata(i,'ybar');
b(i) = sqr(calibdata(i,'xbar1'))/(econdata(i,'p')*qbar(i));

display b1,qbar,b;


***************************************************************************
**************  PART 2. PRODUCTION FUNCTION CALIBRATION  ******************
***************************************************************************

** Set elasticities of substitution between land and N for each crop.
parameters
sigma(i) substitution elasticity by crop and technology
rho(i)   production function elasticity parameter;
sigma(i) = 0.5;
rho(i) = (sigma(i) - 1)/sigma(i);
display rho;

** Ensure that calibration criteria are satisfied. The first criterion
** requires that cc1 > 0 for all i. The second criterion requires that
** cc2 < 0 for all i.
parameters
cc1(i)   calibration criteria 1
flag1(i) flag violations of cc1
psi(i)   term inside cc2
cc2(i)   calibration criteria 2
flag2(i) flag violations of cc2;

cc1(i) = econdata(i,'eta') - cyclesdata(i,'ybarN')/(1 - cyclesdata(i,'ybarN'));
flag1(i) = 1$(cc1(i) lt 0);
abort$(sum(i, flag1(i)) gt 0) "cc1 not satisfied";

psi(i) = sigma(i)*cyclesdata(i,'ybarN')/(econdata(i,'eta')*(1
         - cyclesdata(i,'ybarN')));
cc2(i) = b(i)*econdata(i,'eta')*(1 - psi(i)) - sum(j$(ord(j) ne ord(i)),
         b(j)*econdata(j,'eta')*sqr(1 + (1/econdata(j,'eta')))*(1 + psi(j)
         - cyclesdata(j,'ybarN')));
flag2(i) = 1$(cc2(i) gt 0);
abort$(sum(i,flag2(i)) gt 0) "cc2 not satisfied";

scalars
term     indicator equal to card(i) when all deltas converge /0/
toler    tolerance for convergence /0.001/;

parameters
delta0(i) myopic CES production function parameter
adj(i)    adjustment term using myopic delta
error(i)  absolute value of change in delta
converge(i) indicator equal to one when delta converges;
delta0(i) = econdata(i,'eta')/(1 + econdata(i,'eta'));
adj(i) = 1 - (b(i)/(delta0(i)*(1-delta0(i))))/(sum(j,
         (b(j)/(delta0(j)*(1-delta0(j)))) +
         (sigma(j)*b(j)*cyclesdata(j,'ybarN')/(delta0(j)*(delta0(j)
         - cyclesdata(j,'ybarN'))))));

variables
delta(i)    production function homogeneity parameters
beta(i,l)   production function share parameters
dummy       dummy objective;
positive variables delta,beta;

equations
etacal(i)  calibration to exogenous supply elasticity
nresp(i)   calibration against agronomic yield response to N
betas(i)   summation constraint for share parameters
edummy     dummy objective function;
etacal(i).. econdata(i,'eta') =e= (delta(i)/(1-delta(i)))*adj(i);
Nresp(i).. cyclesdata(i,'ybarN')*((beta(i,'land')*(calibdata(i,'xbar1')**rho(i))) +
          (beta(i,'fertilizer')*(calibdata(i,'xbar2')**rho(i)))) =e=
          delta.l(i)*beta(i,'fertilizer')*(calibdata(i,'xbar2')**rho(i));
betas(i).. sum(l, beta(i,l)) =e= 1;
edummy.. dummy =e= 0;

** Solve supply elasticity system of equations.
model selast /etacal,edummy/;
while(term lt card(i),
solve selast maximizing dummy using nlp;
*Test for convergence in the deltas
         error(i) = abs(delta0(i) - delta.l(i));
         converge(i)$(error(i) lt toler) = 1;
         term = sum(i, converge(i));
*Update values for delta in the adjustment term if convergence test fails
         delta0(i) = delta.l(i);
         adj(i) = 1 - (b(i)/(delta0(i)*(1-delta0(i))))/(sum(j,
                  (b(j)/(delta0(j)*(1-delta0(j)))) +
                  (sigma(j)*b(j)*cyclesdata(j,'ybarN')/(delta0(j)*(delta0(j) - cyclesdata(j,'ybarN'))))));
);

** Solve system of equations for share parameters.
model nelast /nresp,betas,edummy/;
solve nelast maximizing dummy using nlp;
display delta.l,beta.l;

parameters
mu(i)    scale parameters
lbar1    initial shadow value of land
lambda(i,l) calibrated factor shadow values
soccost(i,l) social cost of inputs;

mu(i) =  qbar(i)/((beta.l(i,'land')*(calibdata(i,'xbar1')**rho(i))) +
          (beta.l(i,'fertilizer')*calibdata(i,'xbar2')**rho(i)))**(delta.l(i)/rho(i));
lbar1 = sum(i, (econdata(i,'p')*qbar(i)*(delta.l(i) - cyclesdata(i,'ybarN'))
        - econdata(i,'c1')*calibdata(i,'xbar1'))*calibdata(i,'xbar1'))/sum(i, sqr(calibdata(i,'xbar1')));
lambda(i,'land') = econdata(i,'p')*qbar(i)*(delta.l(i) - cyclesdata(i,'ybarN'))/calibdata(i,'xbar1')
             - (econdata(i,'c1') + lbar1);
lambda(i,'fertilizer') = econdata(i,'p')*qbar(i)*cyclesdata(i,'ybarN')/calibdata(i,'xbar2')
             - econdata(i,'c2');
soccost(i,'land') = econdata(i,'c1') + lbar1 + lambda(i,'land');
soccost(i,'fertilizer') = econdata(i,'c2') + lambda(i,'fertilizer');
display rho,delta.l,beta.l,mu,lbar1,lambda;


***************************************************************************
****************  PART 3. CROP PRODUCTION SIMULATION  *********************
***************************************************************************

table    simdata(i,econ) simulation input data
$ondelim
$include simdata2016.csv
$offdelim
;

parameters
simcost(i,l)     simulated cost of inputs
qbsim(i)         simulated production at baseline (in million kg)
qdiv(i)          MSE divergence from reference level;
simcost(i,'land') = simdata(i,'c1') + lbar1 + lambda(i,'land');
simcost(i,'fertilizer') = simdata(i,'c2') + lambda(i,'fertilizer');
qbsim(i) = mu(i)*((beta.l(i,'land')*(calibdata(i,'xbar1')**rho(i))) +
          (beta.l(i,'fertilizer')*calibdata(i,'xbar2')**rho(i)))**(delta.l(i)/rho(i))/1000000;
qdiv(i) = sqr(abs(qbsim(i) - qbar(i)));
display qbsim,qdiv;

variables
x(i,l)           simulated input use
q(i)             simulated production
qprofit(i)       quasi-profit function
tprofit          total profit;
positive variables x,q,qprofit;

equations
production(i)    production function
quasiprofit(i)   quasi-profit function
obj              objective function
resconl          land constraint
resconf          fertilizer constraint;

production(i).. q(i) =e= mu(i)*(sum(l, beta.l(i,l)*x(i,l)**rho(i)))**(delta.l(i)/rho(i));
quasiprofit(i).. qprofit(i) =e= simdata(i,'p')*q(i) - sum(l, simcost(i,l)*x(i,l));
obj.. tprofit =e= sum(i, qprofit(i));
resconl.. sum(i, x(i,'land')) =e= b1;
resconf.. sum(i, x(i,'fertilizer')) =e= sum(i, calibdata(i,'xbar2'));

x.lo(i,l) = 0.001;

model profitmax /production,quasiprofit,obj,resconl,resconf/;
solve profitmax maximizing tprofit using nlp;

parameters
fertsubsidy(i)   fertilizer subsidy (%)
landarea(i)      land allocation by crop (in ha)
obsyield(i)      yield by crop (in kg per ha)
Nuse(i)          N fertilizer use (in kg per ha);
fertsubsidy(i) = 100*(econdata(i,'c2') - simdata(i,'c2'))/econdata(i,'c2');
landarea(i) = x.l(i,'land');
obsyield(i) = q.l(i)/x.l(i,'land');
Nuse(i) = x.l(i,'fertilizer')/x.l(i,'land');

file     MINTcropsimple /MINTcropsimple.txt/;
MINTcropsimple.pc = 5;
put      MINTcropsimple;
put      'year','region','crop','fert_subsidy (%)','land area (ha)','yield (kg/ha)','production (kg)','Nfert (kg/ha)'/;
loop(i, put '2016', 'pongo', i.tl, fertsubsidy(i), landarea(i), obsyield(i), q.l(i), Nuse(i)/);

