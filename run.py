import os
import shutil


destination_dir = "C:/Users/jacob/Documents/Coding/osProjectMINE/data/1/"


# Remove the sim.data file if it exists
if os.path.exists("stats.csv"):
    os.remove("stats.csv")

# Iterate through the range and run the commands
schuedlerType = 4
for i in range(1, 31):
    os.system(f" python main.py {schuedlerType} {i} 0.06 0.02")
    #print(f" python main.py 1 {i} 0.06")
    if os.path.exists("stats.csv"):
        os.makedirs(destination_dir, exist_ok=True)
        shutil.copy("stats.csv", os.path.join(destination_dir, f"{schuedlerType}-{i}-006quatumIS0.02.csv"))