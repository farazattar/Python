import os
target_dir = 'C:\\Users\\DCS34\\Documents\\temp\\python-prefix-remover'
suffix = '.txt'
os.chdir(target_dir)
directory_list = os.listdir()
for filename in directory_list:    
    if filename.endswith(suffix):
        os.rename(filename, filename[:-len(suffix)])
print("The suffix is removed from the filenames.")
print("The suffix is: " + suffix)
print("The directory is: " + target_dir)