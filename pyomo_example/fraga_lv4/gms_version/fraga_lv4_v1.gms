$title CENG0013 Project Level 4 Cost Model

$ontext
Use the model to investigate the behaviour of the economic potential
in terms of the chosen design variables, considering the annual
hours of operation.

Discuss how the design variables and the decisions you make in
Levels 1 to 4 impact on the economic potential.

Plots of the economic potential with respect to the design
variables will be required to support your discussion.
$offtext

*------------------------------------------------------------------------
* Define the sets of streams and components in the process
*------------------------------------------------------------------------
Set stm Process Streams /Feed1, Feed2, Mixeff, Reacteff, Dist1top,
                     Dist1bot, Purge, LiqRecycle, Prod, Byprod/;

*------------------------------------------------------------------------
* E := Ethylene, P := Propylene, Bz := Benzene,
* Tu := Toluene, EB := Ethylbenzne, DEB := Diethylbenzene
*------------------------------------------------------------------------
Set comp Process Components /E, P, Bz, Tu, EB, DEB/;

*------------------------------------------------------------------------
* Each stream is described by the individual flows of all the components
*------------------------------------------------------------------------
Positive variable
f(stm,comp) Process component flow rates in stream stm [kmol per hr];

*------------------------------------------------------------------------
* Feed 1 (Pure Ethylene stream) and Feed 2 (Benzene stream with Toluene)
*------------------------------------------------------------------------
f.l('Feed1', 'E') = 154.587;
f.fx('Feed1', 'P') = 0;
f.fx('Feed1', 'Bz') = 0;
f.fx('Feed1', 'Tu') = 0;
f.fx('Feed1', 'EB') = 0;
f.fx('Feed1', 'DEB') = 0;

f.fx('Feed2', 'E') = 0;
f.fx('Feed2', 'P') = 0;
f.l('Feed2', 'Bz') = 105.770;
f.l('Feed2', 'Tu') = 5.567;
f.fx('Feed2', 'EB') = 0;
f.fx('Feed2', 'DEB') = 0;

Equation
Feed2Ratio Stoichiometric Ratio in Feed 2;
Feed2Ratio .. f('Feed2', 'Bz') =e= 19 * f('Feed2', 'Tu');

*------------------------------------------------------------------------
* Mixer and Reactor Effluent Initial Values simulated previously
*------------------------------------------------------------------------
f.l('Mixeff', 'E') = 154.587;
f.l('Mixeff', 'P') = 0.011;
f.l('Mixeff', 'Bz') = 184.193;
f.l('Mixeff', 'Tu') = 5.567;
f.l('Mixeff', 'EB') = 0.146;
f.l('Mixeff', 'DEB') = 0;

f.l('Reacteff', 'E') = 2.0665E-4;
f.l('Reacteff', 'P') = 5.578;
f.l('Reacteff', 'Bz') = 78.738;
f.l('Reacteff', 'Tu') = 0;
f.l('Reacteff', 'EB') = 73.171;
f.l('Reacteff', 'DEB') = 37.998;

*------------------------------------------------------------------------
* Distillation Column 1 inlet and outlet Initial Values simulated previously
* Since no Tu HK: EB LK: Bz
*------------------------------------------------------------------------
f.l('Dist1top', 'E') = 2.0665E-4;
f.l('Dist1top', 'P') = 5.578;
f.l('Dist1top', 'Bz') = 78.580;
f.l('Dist1top', 'Tu') = 0;
f.l('Dist1top', 'EB') = 0.146;
f.fx('Dist1top', 'DEB') = 0;

f.fx('Dist1bot', 'E') = 0;
f.fx('Dist1bot', 'P') = 0;
f.l('Dist1bot', 'Bz') = 0.158;
f.l('Dist1bot', 'Tu') = 0;
f.l('Dist1bot', 'EB') = 73.025;
f.l('Dist1bot', 'DEB') = 37.998;

*------------------------------------------------------------------------
* Distillation Column 2 inlet and outlet Initial Values simulated previously
* HK: Bz LK: P
*------------------------------------------------------------------------
f.l('Purge', 'E') = 2.0665E-4;
f.l('Purge', 'P') = 5.567;
f.l('Purge', 'Bz') = 0.157;
f.fx('Purge', 'Tu') = 0;
f.fx('Purge', 'EB') = 0;
f.fx('Purge', 'DEB') = 0;

f.fx('LiqRecycle', 'E') = 0;
f.l('LiqRecycle', 'P') = 0.011;
f.l('LiqRecycle', 'Bz') = 78.423;
f.l('LiqRecycle', 'Tu') = 0;
f.l('LiqRecycle', 'EB') = 0.146;
f.fx('LiqRecycle', 'DEB') = 0;

*------------------------------------------------------------------------
* Distillation Column 3 inlet and outlet Initial Values simulated previously
* HK: DEB LK: EB
*------------------------------------------------------------------------
f.fx('Prod', 'E') = 0;
f.fx('Prod', 'P') = 0;
f.l('Prod', 'Bz') = 0.158;
f.l('Prod', 'Tu') = 0;
f.fx('Prod', 'EB') = 70.560;
f.l('Prod', 'DEB') = 1.282;

f.fx('Byprod', 'E') = 0;
f.fx('Byprod', 'P') = 0;
f.fx('Byprod', 'Bz') = 0;
f.fx('Byprod', 'Tu') = 0;
f.l('Byprod', 'EB') = 2.465;
f.l('Byprod', 'DEB') = 36.715;

*------------------------------------------------------------------------
* Specify a constraint on feasible solutions that they must have a product
* stream with the desired purity of product EB.
*------------------------------------------------------------------------
Parameter purityEB /0.98/;
Equation
fraction Purity of product EB;
fraction .. f('Prod', 'EB') =g= purityEB * sum(comp, f('Prod', comp));

$ontext
Parameters
tearLiqRecycle(comp) Iterated guess of the Liquid Recycle stream [kmol per hr];
tearLiqRecycle('E') = 0;
tearLiqRecycle('P') = 0;
tearLiqRecycle('Bz') = 0;
tearLiqRecycle('Tu') = 0;
tearLiqRecycle('EB') = 0;
tearLiqRecycle('DEB') = 0;
$offtext

*------------------------------------------------------------------------
* Set up the Mixer overall material balance equation
*------------------------------------------------------------------------
Equation mixermb(comp);
mixermb(comp) .. f('Mixeff', comp)
         =e= f('Feed1',comp) + f('Feed2',comp) + f('LiqRecycle',comp);

*------------------------------------------------------------------------
* The reaction requires an excess of Bz, at least more than the flow rate of E
*------------------------------------------------------------------------
Equation reactorfeedconstraint;
reactorfeedconstraint .. f('Mixeff', 'Bz') =g= f('Mixeff', 'E');


*------------------------------------------------------------------------
* The reactions that take place are defined with the single pass conversion, x,
* and one selectivity, S. Both of them depend on the residence time t.
* Later, when a LOOP is used to consider different values of the residence time.
* The conversion and selectivity will be re-calculated.
*------------------------------------------------------------------------
Parameters
S selectivity of EB to DEB [n.d]
x Single pass conversion of EB [n.d]
t Residence time in Reactor [s] /200/;

S = 371.60496 / t + 0.06379;
x = -0.66214 + 0.23303 * log(t);

*------------------------------------------------------------------------
* We will be using extents of reaction mass balances such that we define
* the individual extents here.
*------------------------------------------------------------------------
Positive variables
xi1 Extent of reaction 1,
xi2 Extent of reaction 2,
xi3 Extent of reaction 3;

*xi1.l = 105.455;
*xi2.l = 37.998;
*xi3.l = 5.567;

Equations
selectivitydef  Selectivity (EB DEB) in relation to extent of reactions,
conversiondef   Single pass conversion of Benzene;

selectivitydef .. S * xi2 =e= xi1 - xi2 + xi3;
conversiondef .. x * f('Mixeff', 'Bz') =e= xi1;

*------------------------------------------------------------------------
* Set up individual component mass balacnes of the Reactor
* Set up overall mass balances of the Reactor
* mass balances all of the form: input + generation = output + consumption
* 100% overall conversion of toluene so all toluene is consumed
* Design variable as in Level 2 GAMs simulation
* 100 % overall converstion of Ethylene so all Ethylene is consumed
*------------------------------------------------------------------------
Equations
reactbalE Ethylene mass balacne equation for reactor,
reactbalP Propane mass balacne equation for reactor,
reactbalTu Toluene mass balacne equation for reactor,
reactbalBz Benzene mass balacne equation for reactor,
reactbalEB Ethylbenzene mass balacne equation for reactor,
reactbalDEB Diethylbenzene mass balacne equation for reactor
;

* Ethylene fed and consumed in 1st, 2nd and 3rd reaction
* 100 % overall converstion of Ethylene so all Ethylene is consumed (Hopefully)
reactbalE .. f('Mixeff','E') - xi1 - xi2  - 2 * xi3 =e= f('Reacteff', 'E');

* Propane generated in the 3rd reaction
reactbalP .. f('Mixeff','P') + xi3 =e= f('Reacteff','P');

* Toluene fed and consumed in 3rd reaction
* 100% overall conversion of toluene so all toluene is consumed
reactbalTu .. f('Mixeff','Tu') =e= xi3;

* Benzene consumed in 1st reaction
reactbalBz .. f('Mixeff','Bz') - xi1 =e= f('Reacteff','Bz');

* Ethylbenzene consumed in 2nd reaction & generated from 1st & 3rd reaction
reactbalEB .. f('Mixeff','EB') + xi1 - xi2 + xi3 =e= f('Reacteff', 'EB');

* DEB produced in 2nd reaction
reactbalDEB .. f('Mixeff','DEB') + xi2 =e= f('Reacteff','DEB');

* Initialse values to help GAMs (from level 4 GAMs simulation)
f.l('Reacteff', 'Bz') = 78.738;

*------------------------------------------------------------------------
* The distillation column costing is based on the relative volatilities
* We have calculated the values from Python previously such that we can
* put them here.
*------------------------------------------------------------------------
Parameters
alpha1 Relative volatilities wrt (Bz Light Key EB Heavy Key) /7.9323/
alpha2 Relative volatilities wrt (P Light Key Bz Heavy Key) /469.26539/
alpha3 Relative volatilities wrt (EB Light Key DEB Heavy Key) /8.81191/;

*------------------------------------------------------------------------
* The Distillation Columns 1, 2, and 3 have a design variable respectively.
* We let GAMs to choose the optimal value of the key recovery.
*------------------------------------------------------------------------
Positive variables
r1 recovery of key components in distillation column 1
r2 recovery of key components in distillation column 2
r3 recovery of key components in distillation column 3;

r1.lo = 0.90;
r1.up = 0.998;
r2.lo = 0.90;
r2.up = 0.998;
r3.lo = 0.90;
r3.up = 0.998;

*------------------------------------------------------------------------
* The value of the output stream of the distillation column changes
* depending on the r1 r2 r3 recoveries.
*------------------------------------------------------------------------
Positive Variables
aD1(comp) Presence of chemical species 'comp' in distillation col 1 top stream
aD2(comp) Presence of chemical species 'comp' in distillation col 2 top stream
aD3(comp) Presence of chemical species 'comp' in distillation col 3 top stream
;
aD1.fx('E') = 1;
aD1.fx('P') = 1;
aD1.fx('Tu') = 0;
aD1.fx('DEB') = 0;

aD2.fx('E') = 1;
aD2.fx('Tu') = 0;
aD2.fx('EB') = 0;
aD2.fx('DEB') = 0;

aD3.fx('E') = 1;
aD3.fx('P') = 1;
aD3.fx('Bz') = 1;
aD3.fx('Tu') = 1;

Equations
disttop_lightkey1 Distribution of light key Bz in top stream(Dist1top stream)
disttop_heavykey1 Distribution of heavy key EB to top stream (Dist1top stream)

disttop_lightkey2 Distribution of light key P in top stream (Purge stream)
disttop_heavykey2 Distribution of heavy key Bz to top stream (Purge stream)

disttop_lightkey3 Distribution of light key EB in top stream (Product stream)
disttop_heavykey3 Distribution of heavy key DEB to top stream (Product stream)
;

disttop_lightkey1 .. aD1('Bz') =e= r1;
disttop_heavykey1 .. aD1('EB') =e= 1 - r1;

disttop_lightkey2 .. aD2('P') =e= r2;
disttop_heavykey2 .. aD2('Bz') =e= 1 - r2;

disttop_lightkey3 .. aD3('EB') =e= r3;
disttop_heavykey3 .. aD3('DEB') =e= 1 - r3;

*------------------------------------------------------------------------
* Set up mass balance equations according the definition of
* semi-sharp separation: the recovery of the light and heavy keys.
* Additional assumption includes:
* All non-key species distribute wholly to either top or bottom product.
*------------------------------------------------------------------------
Equations
distmbtop1(comp) Material Bal of the Distillation column 1 top stream
distmbbot1(comp) Material Bal of the Distillation column 1 bot stream
distmbtop2(comp) Material Bal of the Distillation column 2 top stream
distmbbot2(comp) Material Bal of the Distillation column 2 bot stream
distmbtop3(comp) Material Bal of the Distillation column 3 top stream
distmbbot3(comp) Material Bal of the Distillation column 3 bot stream
;
distmbtop1(comp) .. aD1(comp) * f('Reacteff', comp) =e=  f('Dist1top', comp);
distmbbot1(comp).. (1 - aD1(comp)) * f('Reacteff',comp) =e=  f('Dist1bot',comp);

distmbtop2(comp) .. aD2(comp) * f('Dist1top', comp) =e=  f('Purge', comp);
distmbbot2(comp).. (1 - aD2(comp)) * f('Dist1top',comp) =e=  f('LiqRecycle',comp);

distmbtop3(comp) .. aD3(comp) * f('Dist1bot', comp) =e=  f('Prod', comp);
distmbbot3(comp).. (1 - aD3(comp)) * f('Dist1bot',comp) =e=  f('Byprod',comp);

$ontext
*------------------------------------------------------------------------
* Set up Squential Modular Modelling variables
*------------------------------------------------------------------------
Variable
Err Error between LiqRecycle and tearLiqRecycle,
error Free variable;

Parameters
errTol  Error tolerance between LiqRecycle and tearLiqRecycle /0.000001/,
cntTol Iteration Counter tolerance /100/;

Equation
ErrCalRecycle Calculate the error between LiqRecycle and tearLiqRecycle,
dummyeq Dummy Equation to link the free variable error;

ErrCalRecycle .. Err
         =e= sum(comp, (tearLiqRecycle(comp) - f('LiqRecycle',comp)));

dummyeq .. error =e= Err;
*------------------------------------------------------------------------
* Solve Model
*------------------------------------------------------------------------
Model  Level4   /all/;
Scalar cnt  Counter to prevent overshoot /0/;
while (cnt le cntTol,
         Solve Level4 using nlp minimizing error;

         if (abs(Err.l) le errTol, break;
             else tearLiqRecycle(comp) = f.l('LiqRecycle',comp);
         );
         cnt = cnt + 1;
);
$offtext

*------------------------------------------------------------------------
* Cost Calculations
*------------------------------------------------------------------------
Parameters
OHPY Operating Hours Per Year /8150/
OSPY Operating Seconds Per Year;
OSPY = OHPY * 60 * 60;

Parameters
Price(comp) Price of each component [Euro per mol]
/ E 0.05, P 0, Tu 0.10, Bz 0.10, EB 0.25, DEB 0.10/
convfact Conversion factor from [kmol per hr] to [mol per s];
convfact = 1000/60/60;

Parameter
A Heat Exchanger Area [sqm] (Not known as this point without Aspen) /0/;

Positive variables
feed_cost    Cost of Feed 1 and Feed 2  [Million Euros per year]
output_sales Sales of Byproduct and Product  [Million Euros per year]
dist1_c  Cost of Distillation column 1 [Millions Euros per year]
dist2_c  Cost of Distillation column 2 [Millions Euros per year]
dist3_c  Cost of Distillation column 3 [Millions Euros per year]
react_c  Cost of Reactor [Millions Euros per year]
hex_c    Cost of Heat Exchanger [Millions Euros per year];

*------------------------------------------------------------------------
* Material costs and sales based on market prices.
*------------------------------------------------------------------------
Equations
cost_price  Market cost model of the feed
sales_price Market sale model of product and byproducts;

cost_price .. feed_cost * 1e6 / convfact / OSPY
         =e= sum(comp, f('Feed1', comp)) * Price('E')
           + sum(comp, f('Feed2', comp)) * Price('Bz');

sales_price .. output_sales * 1e6 /convfact / OSPY
         =e= sum(comp,f('Byprod', comp)) * Price('DEB')
           + sum(comp,f('Prod', comp)) * Price('EB');

*------------------------------------------------------------------------
* Processing Unit cost
*------------------------------------------------------------------------
Equations
dist1cost Cost model for Distillation column 1
dist2cost Cost model for Distillation column 2
dist3cost Cost model for Distillation column 3
reactcost Cost model for Reactor
hexcost   Cost model for Heat Exchanger;

dist1cost .. dist1_c * 100*(1 - r1)*(alpha1 - 1)
         =e= sqrt(sum(comp, f('Reacteff',comp))* convfact);


dist2cost .. dist2_c * 100*(1 - r2)*(alpha2 - 1)
         =e= sqrt(sum(comp, f('Dist1top',comp))* convfact);


dist3cost .. dist3_c * 100*(1 - r3)*(alpha3 - 1)
         =e= sqrt(sum(comp, f('Dist1bot',comp))* convfact);


reactcost .. react_c * 1000 =e= t * sum(comp,f('Mixeff',comp)) * convfact;

hexcost ..  hex_c * 100 =e= 9 * (A**(0.65));

*------------------------------------------------------------------------
* Overall Economic potential
*------------------------------------------------------------------------
Variables
unitcosts Cost of the all processing units [Million Euros per year]
netvalue Net value of materials [Million Euros per year]
EP Economic Potential [Million of Euros per year];

Equations
mt_costs Calculate the material costs
costunits Calculate the unit costs
economicpotential Calculate the economic potential;

mt_costs.. netvalue  =e= output_sales - feed_cost ;

costunits.. unitcosts =e= dist1_c + dist2_c + dist3_c + react_c + hex_c;

economicpotential .. EP =e= (netvalue  - unitcosts);

*------------------------------------------------------------------------
* We will use the optimization capabilities of GAMs to find the best
* solution for different values of one of the design variables, t, the residence time.
* Letting the optimization method find the best values for the key recoveries
* in the distillation column.
*
* The objective function for the optimization will be the economic potential
* which shoud be maximized.
*------------------------------------------------------------------------
Variable z;
Equation objective Objective Function to maximize EP;
objective .. z =e= EP;
model process /all/;

*------------------------------------------------------------------------
* specify a file to which we will send results
*------------------------------------------------------------------------
file results /cengL4EP.data/;
put results;
put '#      t      r1       r2      r3      x       S       z      status ' /;

*------------------------------------------------------------------------
* iterate over different values of t, the reactor residence time
*------------------------------------------------------------------------
for(t = 5 to 300 by 1,

*------------------------------------------------------------------------
* the selectivity and conversion are a function of the reactor residence time
* and these therefore need to be calculated for each different value of t.
*------------------------------------------------------------------------
S = 371.60496 / t + 0.06379;
x = -0.66214 + 0.23303 * log(t);

*------------------------------------------------------------------------
* we initialize all stream flows to reasonable values to help GAMS get started
* in the search for the solution.
*------------------------------------------------------------------------
f.l(stm,comp) = 10;
f.l('LiqRecycle',comp) = 80 * (1-r2.l);

*------------------------------------------------------------------------
* now solve the model as an optimization problem as there is one degree of
* freedom (the recovery for the semi-sharp split in the distillation column)
*------------------------------------------------------------------------
        solve process using nlp maximizing z;

*------------------------------------------------------------------------
* all relevant values are displayed into the LST file that GAMS generates
*------------------------------------------------------------------------
        display t, r1.l, r2.l, r3.l, x, S, f.l;
        display netvalue.l, unitcosts.l, EP.l;
*------------------------------------------------------------------------
* but for the data file which we can later use to plot the economic potential,
* we will only output those solutions that are feasible
*------------------------------------------------------------------------
        if( (process.modelstat eq 2),
*------------------------------------------------------------------------
* and within those, only those which have a positive economic potential
*------------------------------------------------------------------------
            if( (ep.l >= 0),
                put t, r1.l, r2.l, r3.l, x, S, z.l, process.modelstat /;
            );
        );
    put /;
);


