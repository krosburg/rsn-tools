# RSN Tools
RSN Tools is a collection of tools to make the lives of RSN data team members a little easier. It contains the package `rsn-tools`, which is a compilation of backend modules that help support the remainder of RSN Tools packages and apps, as well as `gap_finder` which is a collection of scripts that can be used to identify, fill, and verify data gaps.

Please see the individual `README.md` files in the various directories of this repository.


## Installation
This installation focuses on getting the `gap_finder` tool up and running. They assume that you already have credentials on the OOINet production and test systems and assume that you have a working Anaconda or Miniconda installation. Here are the steps:

1. Create a new Conda environment with the following packages
```bash
[user@test]: conda create -n rsntools numpy matplotlib requests pip git pandas
```
2. Activate the new environment (if you have an older conda install, use `source activate` instead):
```bash
[user@test]: conda activate rsntools
```

3. Install RSN Tools using pip and git:
```bash
[user@test]: pip install git+https://github.com/krosburg/rsn-tools.git
```

4. Test the installation (this should print a list of reference designators):
```bash
[user@test]: python

>>> from rsn_tools.core.streams import rdList
>>> print(list(rdList.keys()))
>>> quit()
```
 
5. Navigate to the `rsn-tools/core` install in your Anaconda directory (note the python version may be different and `miniconda3` may be `anaconda3`:
```bash
[user@test]: cd ~/miniconda3/envs/rsntools/lib/python3.8/site-packages/rsn_tools/core/
```

6. Copy or move `ooicreds_template.py` to `ooicreds.py`, then use your favorite editor to modify the file to include your M2M API credentials for `prod`, `dev01`, and `dev03`:
```bash
[user@test]: mv ooicreds_template.py ooicreds.py
[user@test]: vim ooicreds.py
```

Replace 'api user key' and 'api user token' for each server with the correct M2M credential. Then change 'username' to your M2M username (usually your email address):
```python
# Production
PROD_CREDENTIALS = ('api user key', 'api user token')

# Pre-Production (dev01)
DEV01_CREDENTIALS = ('api user key', 'api user token')

# UFRAME-3-TEST (dev03)
DEV03_CREDENTIALS = ('api user key', 'api user token')

# Username
OOI_USERNAME = 'username'
```
   
6. With the Conda environment still activated, navigate to a directory where you normally put your git repos (e.g. `/home/krosburg/code/`)

7. Clone the rsn-tools git repo:
```bash
[user@test]: git clone https://github.com/krosburg/rsn-tools/
```

8. Test for correct installation by trying a gap search and NOT doing a playback:
```bash
[user@test]: cd ./rsn-tools/gap_finder/
[user@test]: python rsn_gaps.py --refdes=RS03AXPS-PC03A-4A-DOSTAD303 --times=2019-07 --check-only --preview
```

This should print out a gap playback request (or nothing if no gaps are found), but should not return any errors.