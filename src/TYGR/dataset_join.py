import os
import csv
import subprocess

DATASET_DIR = os.path.join("/src","datasets","generation","O0")
JOIN_DATASET_NAME = "C_CPP_binaries_O0.pkl"
DATALIST_NAME = "C_CPP_binaries_O0.csv"
SAVE_DIR = os.path.join("/src","datasets","generation")
SCRIPT = os.path.join("/src", "TYGR", "TYGR")


os.remove(os.path.join(SAVE_DIR,JOIN_DATASET_NAME))
os.remove(os.path.join(SAVE_DIR, DATALIST_NAME))


files = os.listdir(DATASET_DIR)

with open(os.path.join(SAVE_DIR,DATALIST_NAME),"w") as f:
    write = csv.writer(f)
    write.writerow(files)

if not os.path.isfile(os.path.join(SAVE_DIR,JOIN_DATASET_NAME)):
    print("first_join:",f"{files[0]} + {files[1]}")
    subprocess.run(["bash", SCRIPT, "datamerge", os.path.join(DATASET_DIR,files[0]), os.path.join(DATASET_DIR, files[1]), "-o", os.path.join(SAVE_DIR,JOIN_DATASET_NAME)])

for i in range(len(files)):
    print("add",files[i+2])
    # if i >= 3:
    #     exit()
    subprocess.run(["bash", SCRIPT, "datamerge", os.path.join(DATASET_DIR,files[i+2]), os.path.join(SAVE_DIR,JOIN_DATASET_NAME), "-o", os.path.join(SAVE_DIR,JOIN_DATASET_NAME)])
