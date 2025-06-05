import random

# There are 20 temperature sensors in the circuit
count = 20

# lines list stores all the text that we will put in the params.txt file
lines = []

# Use this to choose which thermistor part number to apply to the simulation
# 1 : 10k@25C B=3380K MF52C1103F3380
# 2 : 100k@25C B=4150 MF52C1104F4150
thermSelect = 1

# Params obtained from:
# https://www.digikey.ca/en/products/detail/cantherm/MF52C1103F3380/1840604
if thermSelect == 1:
    BThermNom = 3380   # Nominal termistor B value
    BThermTol = 0.01   # 1% Tolerance on thermistor
    R0ThermNom = 10000 # Nominal 10k resistance at 25C
    R0ThermTol = 0.01  # % Tolerance on thermistor resistance at 25C

# Params obtained from: 
# https://www.digikey.ca/en/products/detail/cantherm/mf52c1104f4150/1840605
if thermSelect == 2:
    BThermNom = 4150   # Nominal termistor B value
    BThermTol = 0.01   # 1% Tolerance on thermistor
    R0ThermNom = 100000 # Nominal 10k resistance at 25C
    R0ThermTol = 0.01  # % Tolerance on thermistor resistance at 25C

# Add params from selected thermistor to the list
lines.append(f".param BThermNom = {BThermNom}")
lines.append(f".param BThermTol = {BThermTol}")
lines.append(f".param R0ThermNom = {R0ThermNom}")
lines.append(f".param R0ThermTol = {R0ThermTol}")
lines.append(f".param T0Therm = 25+273.15") # R0 of thermisor always measured at T = 25C = 298.19K

# Common node pulldown resistor 
RPdnTol = 0.01
RPdnNom = 100*10**3 # 100k, ** is equal to ^ power operator
lines.append(f".param RPdnTol = {RPdnTol}")
lines.append(f".param RPdnNom = {RPdnNom}")
rv = random.random()
lines.append(f".param Rpdn = {RPdnNom}*(1+2*{RPdnTol}*({rv:.6f} - 0.5)) ;  Actual RPdn = {RPdnNom*(1+2*RPdnTol*(rv - 0.5))}")

# Fixed Resistor 
RFixedTol = 0.01 # % Tolerance on fixed resistor value
RFixedNom = 1*10**3 # Nominal fixed resistor value
lines.append(f".param RFixedTol = {RFixedTol}")
lines.append(f".param RFixedNom = {RFixedNom}")

maxTempVar = 10 # degrees C or K, they're the same size
lines.append(f".param THigh = {maxTempVar} + 5") # maximum temp for prooving the circuit concept

# Generate the parameter lines
for i in range(1, count + 1):

    # Create .param lines for x20 B values with tolerance, append actual value in LTSpice comment
    rv = random.random() # Regenerate random variable for each param
    lines.append(f".param BTherm{i} = {BThermNom}*(1+2*{BThermTol}*({rv:.6f} - 0.5)) ; Actual BTherm{i} = {BThermNom*(1+2*BThermTol*(rv - 0.5))}")

    # .params for thermistor resistance at 25C with tolerance applied
    rv = random.random() # Regenerate random variable for each param
    lines.append(f".param R0Therm{i} = {R0ThermNom}*(1+2*{R0ThermTol}*({rv:.6f} - 0.5)) ; Actual R0Therm{i} = {R0ThermNom*(1+2*R0ThermTol*(rv - 0.5))}")

    # .params for thermistor resistance at 25C with tolerance applied
    rv = random.random() # Regenerate random variable for each param
    lines.append(f".param RFixed{i} = {RFixedNom}*(1+2*{RFixedTol}*({rv:.6f} - 0.5)) ; Actual RFixed{i} = {RFixedNom*(1+2*RFixedTol*(rv - 0.5))}")

    # .params for random temperature variation
    rv = random.random()
    lines.append(f".param T{i} = 2*{maxTempVar}*({rv:.6f} - 0.5) ; Actual T{i} = {2*maxTempVar*(rv - 0.5)}")
    

# Write to params.txt
file_path = "params.txt"
with open(file_path, "w") as f:
    f.write("\n".join(lines))