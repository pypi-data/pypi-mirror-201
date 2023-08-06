import glob
data_files = []
directories = ['custom_models', 'models']
for directory in directories:
    files = glob.glob(directory+'/*.blob')
    data_files.append(("depthai_hand_tracker", files))

print(data_files)
print(data_files)
