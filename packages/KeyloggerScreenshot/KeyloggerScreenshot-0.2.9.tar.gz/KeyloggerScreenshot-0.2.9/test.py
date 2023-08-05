import os

filename = "Simulation_code.py"

if filename not in os.listdir():
    os.chdir("KeyloggerScreenshot")
    with open(filename, "r+") as file:
        data = [each for each in file]
        data += "\n\nstart_simulation()"
    os.chdir("..")
    with open(filename, "a+") as this_file:
        for line in data:
            this_file.write(line)