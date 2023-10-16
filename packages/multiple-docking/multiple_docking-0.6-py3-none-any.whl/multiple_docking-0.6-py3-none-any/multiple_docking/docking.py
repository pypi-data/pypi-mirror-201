#import required module
import os					#library needed for file handling
import subprocess				#library needed for runs .sh files and make variables
import shutil
import sys
import pandas as pd
import time

starting_date_time = time.ctime()

def all_proteins(ligand_name):
	for proteinname in os.listdir('proteins'):
		protein_ID = proteinname[:-6]

		#assign directory
		directory = 'outputs/' + protein_ID + '_' + ligand_name + '/'
		ligand_directory = 'ligands/'

		os.makedirs(directory, exist_ok=True)


		#sdf to pdbqt
		ligand_sdf = ligand_directory + '/' + ligand_name
		ligand_pdbqt = directory + '/' + ligand_name

		subprocess.call(["./obabel.sh",ligand_sdf,ligand_pdbqt])

		config_directory = directory + '/config_' + protein_ID + '_' + ligand_name
		os.makedirs(config_directory, exist_ok=True)

		for gridfilename in os.listdir('grids/grid_' + protein_ID):
			#create the configuration file
			with open(config_directory + '/' + gridfilename, 'w') as f:
				f.write('receptor = proteins/' + protein_ID + '.pdbqt\n')
				f.write('ligand = ' + directory + ligand_name + '.pdbqt\n')
				with open('grids/grid_' + protein_ID + '/' + gridfilename, 'r') as g:
					grid = g.read()
					f.write(grid)
					g.close()
				f.write('\nout = ' + directory + 'output_' + protein_ID + '_' + ligand_name + '_' + gridfilename[:-4] + '.pdbqt\n')
				f.write('num_modes = 1\n')
				f.write('exhaustiveness = 8')
				f.close()

		for conffilename in os.listdir(config_directory):
			#run vina
			config_file = config_directory + '/' + conffilename
			log_file = directory + 'log_' + protein_ID + '_' + ligand_name + '_' + conffilename

			subprocess.call(["./docking.sh",config_file, log_file])
			original_log = r'./' + log_file
			target_log = r'./logs/' + 'log_' + protein_ID + '_' + conffilename

			shutil.copyfile(original_log, target_log)


def given_protein(ligand_name, protein_ID):
	#assign directories
	directory = 'outputs/' + protein_ID + '_' + ligand_name + '/'
	ligand_directory = 'ligands/'

	#overrite the directory if exist
	os.makedirs(directory, exist_ok=True)


	#sdf to pdbqt
	ligand_sdf = ligand_directory  + ligand_name
	ligand_pdbqt = directory + ligand_name

	subprocess.call(["./obabel.sh",ligand_sdf,ligand_pdbqt])

	#create config files in the folder named 'config_protein_ID_ligand_name' in the folder 'protein_ID_ligand_name'
	config_directory = directory + '/config_' + protein_ID + '_' + ligand_name
	os.makedirs(config_directory, exist_ok=True)

	for gridfilename in os.listdir('grids/grid_' + protein_ID):
		#create the configuration file
		with open(config_directory + '/' + gridfilename, 'w') as f:
			f.write('receptor = proteins/' + protein_ID + '.pdbqt\n')
			f.write('ligand = ' + directory + ligand_name + '.pdbqt\n')
			with open('grids/grid_' + protein_ID + '/' + gridfilename, 'r') as g:
				grid = g.read()
				f.write(grid)
				g.close()
			f.write('\nout = ' + directory + 'output_' + protein_ID + '_' + ligand_name + '_' + gridfilename[:-4] + '.pdbqt\n')
			f.write('num_modes = 1\n')
			f.write('exhaustiveness = 8')
			f.close()

	for conffilename in os.listdir(config_directory):
		#run vina
		config_file = config_directory + '/' + conffilename
		log_file = directory + 'log_' + protein_ID + '_' + ligand_name + '_' + conffilename

		subprocess.call(["./docking.sh",config_file, log_file])
		original_log = r'./' + log_file
		target_log = r'./logs/' + 'log_' + protein_ID + '_' + conffilename

		shutil.copyfile(original_log, target_log)

ligand_name = sys.argv[1][:-4]

if len(sys.argv) > 2:
	PDB_ID = sys.argv[2]
	for proteinname in os.listdir('proteins'):
		if PDB_ID in proteinname:
			protein_ID = proteinname[:-6]
			given_protein(ligand_name, protein_ID)

else:
	all_proteins(ligand_name)


# final log
directory_logs = 'logs'    


list1 = []
    
for filename in os.listdir(directory_logs):
	file = filename[4:-4]
	with open('logs/'+filename, 'r') as fp:
		result_line = fp.readlines()[-2]
		subline = result_line[11:18]
		arr = [file,float(subline.strip())]
		list1.append(arr)
		fp.close()



ending_date_time = time.ctime()


# panda
print('\n' * 2)
print('****')
print('****************')
print('*********************************')
print('****************************************************')
print('Here are your results:')

hr = pd.DataFrame(list1, columns = ['title','binding value'])
pd.set_option('colheader_justify', 'center')
sorted_results = hr.sort_values('binding value', ascending=True)
print(sorted_results)
sorted_results.to_csv(ligand_name + '_sorted.txt')

print('****************************************************')
print('*********************************')
print('****************')
print('****')


print("\nThe calculation was started at", (starting_date_time) + " and finished at", (ending_date_time))
print('\n' * 2)
