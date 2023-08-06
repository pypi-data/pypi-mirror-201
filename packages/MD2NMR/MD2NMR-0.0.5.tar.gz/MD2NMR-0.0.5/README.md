# MD2NMR. 
Written by TW on Jan 2023, Queen's University Panchenko's Lab.
For any enquiries please contact anna.panchenko@queensu.ca. back up email: t.wei@queensu.ca 

Tools for calculating NMR relaxation observables (R1/R2/NOE/T1/T2/Tau_c) directly from MD trajectories. Initially written for calculations regarding nucleosome simulations but can be extended for other proteins/complexes. This software is subject to MIT license, with some functions imported from other repo, as noted individually in script comment section.

Dependencies:
The required packages are listed in 'requirements.txt'.
To create a new environment using anaconda: (replace myenv as approperiate)
conda create --name myenv --file requirements.txt

or use pip:
pip install virtualenv #create virtual environment
virtualenv test_env  
source test_env/bin/activate
pip install numpy==1.23.4 pandas==1.5.1 scikit-learn==1.1.3 scipy==1.9.3 mdtraj==1.9.7

Usage:
For single file mode (basic usage):
python md2nmr.py -t {$topology_file$} -y {$trajectory_file_path$}


Before usage one should first check the config.py and make sure the parameters are suitable for the calculation. change the prefix list and working directory/output directory as needed.

Double check the magnetic field strength is corresponding to experiment result: B0 in md2nmr.py file.

To test: use the following command to download a testing MD traj under './data' directory.
then run following command to test. result should be in the output directory.
python ./src/md2nmr.py -t H2A.pdb -y H2A_1.xtc 

then change the $use_chain_ids$ in config.py to "use_chain_ids = False" and run:
to test on the other trajectory.
python ./src/md2nmr.py -t vanilla_run1.pdb -y vanilla_run1.xtc


for batch mode: check the config file and modify the prefix list var in it.
Note that the batch mode will generate results for all traj/topo under working directory with satisfied prefix.
then in command line:
python main.py --batch=True


