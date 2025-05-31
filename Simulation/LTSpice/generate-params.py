import random

count = 20

## Thermistor
BThermNom = 3380   # 
BThermTol = 0.01   # 1% Tolerance on thermistor
R0ThermNom = 10000 # Nominal 10k resistance at 25C
R0ThermTol = 0.01  # % Tolerance on thermistor resistance at 25C

## Fixed Resistor
RFixedNom = 1000 # Nominal fixed resistor value 
RFixedTol = 0.01 # % Tolerance on fixed resistor value

# Generate the parameter lines
lines = []
for i in range(1, count + 1):

    # Create .param lines for x20 B values with tolerance
    lines.append(f".param BTherm{i} = {BThermNom}*(1+2*{BThermTol}*({random.random():.6f} - 0.5))")

    # .params for thermistor resistance at 25C with tolerance applied
    lines.append(f".param R0Therm{i} = {R0ThermNom}*(1+2*{R0ThermTol}*({random.random():.6f} - 0.5))")

    # .params for thermistor resistance at 25C with tolerance applied
    lines.append(f".param RFixed{i} = {RFixedNom}*(1+2*{RFixedTol}*({random.random():.6f} - 0.5))")



# Write to params.txt
file_path = "params.txt"
with open(file_path, "w") as f:
    f.write("\n".join(lines))
