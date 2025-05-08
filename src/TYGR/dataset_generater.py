import os
import json
import subprocess

DATASET_DIR = os.path.join("/src", "datasets", "x86_64", "c_cpp")
SAVE_DIR = os.path.join("/src", "datasets", "generation", "O0")
TARGET_JSON = os.path.join("/src", "datasets", "x86_64", "C_CPP_binaries_O0.json")
SCRIPT = os.path.join("/src", "TYGR", "TYGR")

with open(TARGET_JSON, "r") as f:
    data = json.load(f)

files = os.listdir(SAVE_DIR)

print("files in save dir:", files)

for target_path in data.keys():
    input_path = os.path.join(DATASET_DIR, target_path)
    file_name = os.path.basename(target_path)

    if file_name+".pkl" in files:
        print("already exists:", file_name)
        continue

    output_path = os.path.join(SAVE_DIR, file_name+".pkl")


    print("processing:", input_path)
    subprocess.run(["bash", SCRIPT, "datagen", input_path, output_path])
    #exit(0)