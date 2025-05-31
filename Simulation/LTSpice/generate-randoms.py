import random

def generate_params(filename="params.txt", count=200):
    with open(filename, "w") as f:
        for i in range(1, count + 1):
            value = round(random.random(), 6)
            f.write(f".param random{i} = {value:.6f}\n")

# Run the function to generate the file
regenerate_randoms_file()