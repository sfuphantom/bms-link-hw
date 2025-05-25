%% Written by Dan Renardson of Team Phantom BMS 
%{

% This simulation is to be used in choosing components for the BMS links
% The circuit used here is a set of diode paralleled thermistors

[5V Regulator]
 |
 |
[NTC Thermistor]----[Resistor]----[GND]
                 |
                x20
                 |
          [Common Comparator Input]->[Output to BMS Links]
                 |
                 |
        [Pulldown Resistor]
                 |
                 |
               [GND]
%}

%% Inital Cleanup
clc
close all
%clear all

%% Global Parameters
t = 0:0.1:180;             % Time from zero to 3 minutes in 100 ms increments
vsupply.v = 5;               % Voltage divider supplied with 5V
vsupply.tol = 0.1;         % Voltage regulator tolerance
tmin = 0;                 % Minimum temperature in degrees C
tmax = 70;                 % Maximum temperature in degrees C
                           % Convert these to Kelvin by adding 273.15

% Compute linear temperature rise in degrees C
temperature = tmin + ((tmax-tmin)./max(t))*t;


%% Resistor Parameters
res.r = 10*10.^3;   % Nominal resistor value in Ohms
res.tol = 0.05;     % Two-sided tolerance of the resistor
res.pmax = 0.1;     % Maximum resistor power in Watts 

%% Thermistor Parameters
% https://www.digikey.ca/en/products/detail/cantherm/MF52C1103F3380/1840604
therm.b = 3380;              % Thermistor B value in K
therm.btol = 0.01;           % Two-sided B balue tolerance
therm.r0 = 10*10^3;          % Thermistor resistance in Ohms at t0 degrees C
therm.rtol = 0.01;           % Two-sided resistance @25C tolerance
therm.t0 = 25;               % Given temperature for 10 kOhm
therm.rmax = zeros(size(t)); % Initialize thermistor resistance arrays
therm.rmin = zeros(size(t));

%% Diode Parameters


%% Pulldown Resistor Parameters
pdn.r = 10*10.^3; % Nominal resistor value in Ohms
pdn.tol = 0.05;    % Two-sided tolerance of the resistor



%% Thermistor Resistance Calculations 

% Compute maximum thermistor resistance in Ohms for temperature range
therm.rmax = (therm.r0 + (therm.r0*therm.rtol)).*...               % Max resistance @25C given tolerance
             (exp((therm.b + (therm.b*therm.btol)).* ...           % Max B given tolerance
             (1./(temperature+273.15) - 1./(therm.t0+273.15))));   % Convert temperatures to Kelivn


% Compute maximum thermistor resistance in Ohms for temperature range
therm.rmin = (therm.r0 - (therm.r0*therm.rtol)).*...               % Max resistance @25C given tolerance
             (exp((therm.b - (therm.b*therm.btol)).* ...           % Max B given tolerance
             (1./(temperature+273.15) - 1./(therm.t0+273.15))));   % Convert temperatures to Kelivn


%% Voltage Divider Calculations

% Compute maximum voltage at the voltage divider node 
% This case takes min thermistor resistance, max fixed resistance, max supply voltage
vsense.vmax = (vsupply.v + vsupply.v*vsupply.tol).*(res.r + res.r*res.tol)./...
              (res.r + res.r*res.tol + therm.rmin);

% Compute minimum voltage at the voltage divider node 
% This case takes max thermistor resistance, min fixed resistance, min supply voltage
vsense.vmin = (vsupply.v - vsupply.v*vsupply.tol).*(res.r - res.r*res.tol)./...
              (res.r - res.r*res.tol + therm.rmax);


%% Plots
figure; hold on
plot(temperature, therm.rmax, Color="blue", LineWidth=1.5)
plot(temperature, therm.rmin, Color="red", LineWidth=1.5)
legend("Maximum Resistance", "Minimum Resistance")
xlabel("Cell Temperature (°C)");
ylabel("Thermistor Resistance (Ω)");
ylim([0, 30.*10.^3])

hold off; figure; hold on
plot(temperature, vsense.vmax, Color="blue", LineWidth=1.5)
plot(temperature, vsense.vmin, Color="red", LineWidth=1.5)
legend("Maximum Voltage", "Minimum Voltage");
xlabel("Cell Temperature (°C)");
ylabel("Sensor Voltage (V)");
