%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%                                                                  %%%%%
%%%%    IEEE PES Power Grid Library - Optimal Power Flow - v21.07     %%%%%
%%%%          (https://github.com/power-grid-lib/pglib-opf)           %%%%%
%%%%               Benchmark Group - Typical Operations               %%%%%
%%%%                         29 - July - 2021                         %%%%%
%%%%                                                                  %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Power flow data for the IEEE RELIABILITY TEST SYSTEM 1979.
%
%   IEEE Reliability Test System Task Force of the Applications of
%   Probability Methods Subcommittee, "IEEE reliability test system,"
%   IEEE Transactions on Power Apparatus and Systems, Vol. 98, No. 6,
%   Nov./Dec. 1979, pp. 2047-2054.
%
%   Cost data is from Web site run by Georgia Tech Power Systems Control
%   and Automation Laboratory:
%       http://pscal.ece.gatech.edu/testsys/index.html
%
%   Matpower case file data provided by Bruce Wollenberg.
%
%   Copyright (c) 1979 The Institute of Electrical and Electronics Engineers (IEEE)
%   Licensed under the Creative Commons Attribution 4.0
%   International license, http://creativecommons.org/licenses/by/4.0/
%
%   Contact M.E. Brennan (me.brennan@ieee.org) for inquries on further reuse of
%   this dataset.
%
function mpc = pglib_opf_case24_ieee_rts
mpc.version = '2';
mpc.baseMVA = 100.0;

%% area data
%	area	refbus
mpc.areas = [
	1	 1;
	2	 3;
	3	 8;
	4	 6;
];

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [
	1	 2	 108.0	 22.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	2	 2	 97.0	 20.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	3	 1	 180.0	 37.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	4	 1	 74.0	 15.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	5	 1	 71.0	 14.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	6	 1	 136.0	 28.0	 0.0	 -100.0	 2	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	7	 2	 125.0	 25.0	 0.0	 0.0	 2	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	8	 1	 171.0	 35.0	 0.0	 0.0	 2	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	9	 1	 175.0	 36.0	 0.0	 0.0	 1	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	10	 1	 195.0	 40.0	 0.0	 0.0	 2	    1.00000	    0.00000	 138.0	 1	    1.05000	    0.95000;
	11	 1	 0.0	 0.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	12	 1	 0.0	 0.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	13	 3	 265.0	 54.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	14	 2	 194.0	 39.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	15	 2	 317.0	 64.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	16	 2	 100.0	 20.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	17	 1	 0.0	 0.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	18	 2	 333.0	 68.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	19	 1	 181.0	 37.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	20	 1	 128.0	 26.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	21	 2	 0.0	 0.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	22	 2	 0.0	 0.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	23	 2	 0.0	 0.0	 0.0	 0.0	 3	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
	24	 1	 0.0	 0.0	 0.0	 0.0	 4	    1.00000	    0.00000	 230.0	 1	    1.05000	    0.95000;
];

%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin
mpc.gen = [
	1	 18.0	 5.0	 10.0	 0.0	 1.0	 100.0	 1	 20.0	 16.0;
	1	 18.0	 5.0	 10.0	 0.0	 1.0	 100.0	 1	 20.0	 16.0;
	1	 45.6	 2.5	 30.0	 -25.0	 1.0	 100.0	 1	 76.0	 15.2;
	1	 45.6	 2.5	 30.0	 -25.0	 1.0	 100.0	 1	 76.0	 15.2;
	2	 18.0	 5.0	 10.0	 0.0	 1.0	 100.0	 1	 20.0	 16.0;
	2	 18.0	 5.0	 10.0	 0.0	 1.0	 100.0	 1	 20.0	 16.0;
	2	 45.6	 2.5	 30.0	 -25.0	 1.0	 100.0	 1	 76.0	 15.2;
	2	 45.6	 2.5	 30.0	 -25.0	 1.0	 100.0	 1	 76.0	 15.2;
	7	 62.5	 30.0	 60.0	 0.0	 1.0	 100.0	 1	 100.0	 25.0;
	7	 62.5	 30.0	 60.0	 0.0	 1.0	 100.0	 1	 100.0	 25.0;
	7	 62.5	 30.0	 60.0	 0.0	 1.0	 100.0	 1	 100.0	 25.0;
	13	 133.0	 40.0	 80.0	 0.0	 1.0	 100.0	 1	 197.0	 69.0;
	13	 133.0	 40.0	 80.0	 0.0	 1.0	 100.0	 1	 197.0	 69.0;
	13	 133.0	 40.0	 80.0	 0.0	 1.0	 100.0	 1	 197.0	 69.0;
	14	 0.0	 75.0	 200.0	 -50.0	 1.0	 100.0	 1	 0.0	 0.0;
	15	 7.2	 3.0	 6.0	 0.0	 1.0	 100.0	 1	 12.0	 2.4;
	15	 7.2	 3.0	 6.0	 0.0	 1.0	 100.0	 1	 12.0	 2.4;
	15	 7.2	 3.0	 6.0	 0.0	 1.0	 100.0	 1	 12.0	 2.4;
	15	 7.2	 3.0	 6.0	 0.0	 1.0	 100.0	 1	 12.0	 2.4;
	15	 7.2	 3.0	 6.0	 0.0	 1.0	 100.0	 1	 12.0	 2.4;
	15	 104.65	 15.0	 80.0	 -50.0	 1.0	 100.0	 1	 155.0	 54.3;
	16	 104.65	 15.0	 80.0	 -50.0	 1.0	 100.0	 1	 155.0	 54.3;
	18	 250.0	 75.0	 200.0	 -50.0	 1.0	 100.0	 1	 400.0	 100.0;
	21	 250.0	 75.0	 200.0	 -50.0	 1.0	 100.0	 1	 400.0	 100.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	22	 30.0	 3.0	 16.0	 -10.0	 1.0	 100.0	 1	 50.0	 10.0;
	23	 104.65	 15.0	 80.0	 -50.0	 1.0	 100.0	 1	 155.0	 54.3;
	23	 104.65	 15.0	 80.0	 -50.0	 1.0	 100.0	 1	 155.0	 54.3;
	23	 245.0	 62.5	 150.0	 -25.0	 1.0	 100.0	 1	 350.0	 140.0;
];

%% generator cost data
%	2	startup	shutdown	n	c(n-1)	...	c0
mpc.gencost = [
	2	 1500.0	 0.0	 3	   0.000000	 130.000000	 400.684900;
	2	 1500.0	 0.0	 3	   0.000000	 130.000000	 400.684900;
	2	 1500.0	 0.0	 3	   0.014142	  16.081100	 212.307600;
	2	 1500.0	 0.0	 3	   0.014142	  16.081100	 212.307600;
	2	 1500.0	 0.0	 3	   0.000000	 130.000000	 400.684900;
	2	 1500.0	 0.0	 3	   0.000000	 130.000000	 400.684900;
	2	 1500.0	 0.0	 3	   0.014142	  16.081100	 212.307600;
	2	 1500.0	 0.0	 3	   0.014142	  16.081100	 212.307600;
	2	 1500.0	 0.0	 3	   0.052672	  43.661500	 781.521000;
	2	 1500.0	 0.0	 3	   0.052672	  43.661500	 781.521000;
	2	 1500.0	 0.0	 3	   0.052672	  43.661500	 781.521000;
	2	 1500.0	 0.0	 3	   0.007170	  48.580400	 832.757500;
	2	 1500.0	 0.0	 3	   0.007170	  48.580400	 832.757500;
	2	 1500.0	 0.0	 3	   0.007170	  48.580400	 832.757500;
	2	 1500.0	 0.0	 3	   0.000000	   0.000000	   0.000000;
	2	 1500.0	 0.0	 3	   0.328412	  56.564000	  86.385200;
	2	 1500.0	 0.0	 3	   0.328412	  56.564000	  86.385200;
	2	 1500.0	 0.0	 3	   0.328412	  56.564000	  86.385200;
	2	 1500.0	 0.0	 3	   0.328412	  56.564000	  86.385200;
	2	 1500.0	 0.0	 3	   0.328412	  56.564000	  86.385200;
	2	 1500.0	 0.0	 3	   0.008342	  12.388300	 382.239100;
	2	 1500.0	 0.0	 3	   0.008342	  12.388300	 382.239100;
	2	 1500.0	 0.0	 3	   0.000213	   4.423100	 395.374900;
	2	 1500.0	 0.0	 3	   0.000213	   4.423100	 395.374900;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.000000	   0.001000	   0.001000;
	2	 1500.0	 0.0	 3	   0.008342	  12.388300	 382.239100;
	2	 1500.0	 0.0	 3	   0.008342	  12.388300	 382.239100;
	2	 1500.0	 0.0	 3	   0.004895	  11.849500	 665.109400;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
	1	 2	 0.0026	 0.0139	 0.4611	 175.0	 193.0	 200.0	 0.0	 0.0	 1	 -30.0	 30.0;
	1	 3	 0.0546	 0.2112	 0.0572	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	1	 5	 0.0218	 0.0845	 0.0229	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	2	 4	 0.0328	 0.1267	 0.0343	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	2	 6	 0.0497	 0.192	 0.052	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	3	 9	 0.0308	 0.119	 0.0322	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	3	 24	 0.0023	 0.0839	 0.0	 400.0	 510.0	 600.0	 1.03	 0.0	 1	 -30.0	 30.0;
	4	 9	 0.0268	 0.1037	 0.0281	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	5	 10	 0.0228	 0.0883	 0.0239	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	6	 10	 0.0139	 0.0605	 2.459	 175.0	 193.0	 200.0	 0.0	 0.0	 1	 -30.0	 30.0;
	7	 8	 0.0159	 0.0614	 0.0166	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	8	 9	 0.0427	 0.1651	 0.0447	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	8	 10	 0.0427	 0.1651	 0.0447	 175.0	 208.0	 220.0	 0.0	 0.0	 1	 -30.0	 30.0;
	9	 11	 0.0023	 0.0839	 0.0	 400.0	 510.0	 600.0	 1.03	 0.0	 1	 -30.0	 30.0;
	9	 12	 0.0023	 0.0839	 0.0	 400.0	 510.0	 600.0	 1.03	 0.0	 1	 -30.0	 30.0;
	10	 11	 0.0023	 0.0839	 0.0	 400.0	 510.0	 600.0	 1.02	 0.0	 1	 -30.0	 30.0;
	10	 12	 0.0023	 0.0839	 0.0	 400.0	 510.0	 600.0	 1.02	 0.0	 1	 -30.0	 30.0;
	11	 13	 0.0061	 0.0476	 0.0999	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	11	 14	 0.0054	 0.0418	 0.0879	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	12	 13	 0.0061	 0.0476	 0.0999	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	12	 23	 0.0124	 0.0966	 0.203	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	13	 23	 0.0111	 0.0865	 0.1818	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	14	 16	 0.005	 0.0389	 0.0818	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	15	 16	 0.0022	 0.0173	 0.0364	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	15	 21	 0.0063	 0.049	 0.103	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	15	 21	 0.0063	 0.049	 0.103	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	15	 24	 0.0067	 0.0519	 0.1091	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	16	 17	 0.0033	 0.0259	 0.0545	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	16	 19	 0.003	 0.0231	 0.0485	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	17	 18	 0.0018	 0.0144	 0.0303	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	17	 22	 0.0135	 0.1053	 0.2212	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	18	 21	 0.0033	 0.0259	 0.0545	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	18	 21	 0.0033	 0.0259	 0.0545	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	19	 20	 0.0051	 0.0396	 0.0833	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	19	 20	 0.0051	 0.0396	 0.0833	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	20	 23	 0.0028	 0.0216	 0.0455	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	20	 23	 0.0028	 0.0216	 0.0455	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
	21	 22	 0.0087	 0.0678	 0.1424	 500.0	 600.0	 625.0	 0.0	 0.0	 1	 -30.0	 30.0;
];

% INFO    : === Translation Options ===
% INFO    : Phase Angle Bound:           30.0 (deg.)
% INFO    : Setting Flat Start
% INFO    : 
% INFO    : === Generator Bounds Update Notes ===
% INFO    : 
% INFO    : === Base KV Replacement Notes ===
% INFO    : 
% INFO    : === Transformer Setting Replacement Notes ===
% INFO    : 
% INFO    : === Line Capacity Monotonicity Notes ===
% INFO    : 
% INFO    : === Voltage Setpoint Replacement Notes ===
% INFO    : Bus 1	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 2	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 3	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 4	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 5	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 6	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 7	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 8	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 9	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 10	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 11	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 12	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 13	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 14	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 15	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 16	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 17	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 18	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 19	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 20	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 21	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 22	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 23	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : Bus 24	: V=1.0, theta=0.0 -> V=1.0, theta=0.0
% INFO    : 
% INFO    : === Generator Setpoint Replacement Notes ===
% INFO    : Gen at bus 1	: Pg=10.0, Qg=0.0 -> Pg=18.0, Qg=5.0
% INFO    : Gen at bus 1	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 1	: Pg=10.0, Qg=0.0 -> Pg=18.0, Qg=5.0
% INFO    : Gen at bus 1	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 1	: Pg=76.0, Qg=0.0 -> Pg=45.6, Qg=2.5
% INFO    : Gen at bus 1	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 1	: Pg=76.0, Qg=0.0 -> Pg=45.6, Qg=2.5
% INFO    : Gen at bus 1	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 2	: Pg=10.0, Qg=0.0 -> Pg=18.0, Qg=5.0
% INFO    : Gen at bus 2	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 2	: Pg=10.0, Qg=0.0 -> Pg=18.0, Qg=5.0
% INFO    : Gen at bus 2	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 2	: Pg=76.0, Qg=0.0 -> Pg=45.6, Qg=2.5
% INFO    : Gen at bus 2	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 2	: Pg=76.0, Qg=0.0 -> Pg=45.6, Qg=2.5
% INFO    : Gen at bus 2	: Vg=1.035 -> Vg=1.0
% INFO    : Gen at bus 7	: Pg=80.0, Qg=0.0 -> Pg=62.5, Qg=30.0
% INFO    : Gen at bus 7	: Vg=1.025 -> Vg=1.0
% INFO    : Gen at bus 7	: Pg=80.0, Qg=0.0 -> Pg=62.5, Qg=30.0
% INFO    : Gen at bus 7	: Vg=1.025 -> Vg=1.0
% INFO    : Gen at bus 7	: Pg=80.0, Qg=0.0 -> Pg=62.5, Qg=30.0
% INFO    : Gen at bus 7	: Vg=1.025 -> Vg=1.0
% INFO    : Gen at bus 13	: Pg=95.1, Qg=0.0 -> Pg=133.0, Qg=40.0
% INFO    : Gen at bus 13	: Vg=1.02 -> Vg=1.0
% INFO    : Gen at bus 13	: Pg=95.1, Qg=0.0 -> Pg=133.0, Qg=40.0
% INFO    : Gen at bus 13	: Vg=1.02 -> Vg=1.0
% INFO    : Gen at bus 13	: Pg=95.1, Qg=0.0 -> Pg=133.0, Qg=40.0
% INFO    : Gen at bus 13	: Vg=1.02 -> Vg=1.0
% INFO    : Gen at bus 14	: Pg=0.0, Qg=35.3 -> Pg=0.0, Qg=75.0
% INFO    : Gen at bus 14	: Vg=0.98 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=12.0, Qg=0.0 -> Pg=7.2, Qg=3.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=12.0, Qg=0.0 -> Pg=7.2, Qg=3.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=12.0, Qg=0.0 -> Pg=7.2, Qg=3.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=12.0, Qg=0.0 -> Pg=7.2, Qg=3.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=12.0, Qg=0.0 -> Pg=7.2, Qg=3.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 15	: Pg=155.0, Qg=0.0 -> Pg=104.65, Qg=15.0
% INFO    : Gen at bus 15	: Vg=1.014 -> Vg=1.0
% INFO    : Gen at bus 16	: Pg=155.0, Qg=0.0 -> Pg=104.65, Qg=15.0
% INFO    : Gen at bus 16	: Vg=1.017 -> Vg=1.0
% INFO    : Gen at bus 18	: Pg=400.0, Qg=0.0 -> Pg=250.0, Qg=75.0
% INFO    : Gen at bus 18	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 21	: Pg=400.0, Qg=0.0 -> Pg=250.0, Qg=75.0
% INFO    : Gen at bus 21	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 22	: Pg=50.0, Qg=0.0 -> Pg=30.0, Qg=3.0
% INFO    : Gen at bus 22	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 23	: Pg=155.0, Qg=0.0 -> Pg=104.65, Qg=15.0
% INFO    : Gen at bus 23	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 23	: Pg=155.0, Qg=0.0 -> Pg=104.65, Qg=15.0
% INFO    : Gen at bus 23	: Vg=1.05 -> Vg=1.0
% INFO    : Gen at bus 23	: Pg=350.0, Qg=0.0 -> Pg=245.0, Qg=62.5
% INFO    : Gen at bus 23	: Vg=1.05 -> Vg=1.0
% INFO    : 
% INFO    : === Writing Matpower Case File Notes ===
