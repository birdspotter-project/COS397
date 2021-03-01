[![Build Status](https://cloud.drone.io/api/badges/devinchristianson/COS397/status.svg)](https://cloud.drone.io/devinchristianson/COS397) [![codecov](https://codecov.io/gh/devinchristianson/COS397/branch/master/graph/badge.svg?token=21BMX3EDC6)](https://codecov.io/gh/devinchristianson/COS397)
# BirdSpotter
BirdSpotter is a graphical interface for integrating and viewing machine learning and field survey data for rapid population estimation of colonial nesting birds. The creation of this interface will allow officials to quickly and effectively draw conclusions based on data provided from human and machine learning observations of bird species, activity, and location. 

### Deliverables
- [Software Requirements Specification](Documentation/Deliverables/Software_Requirements_Specification/SRS.pdf)
- [Software Design Document](Documentation/Deliverables/Software_Design_Document/SDD.pdf)
- [UI Design Document](Documentation/Deliverables/UI_Design_Document/UIDD.pdf)
- [Critical Design Review](https://github.com/devinchristianson/COS397/blob/master/Documentation/Deliverables/CDR.pdf)

### Manual Development 
#### Setup Instructions
1. Clone the repository
2. It is recommended to create a virtual environment for development
	- For installation instructions view this [page](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. Install miniconda (https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
4. Install GDAL: `conda install gdal`
5. Correct dependencies: `conda update numpy`
6. Once in the desired environment install required packages by running `pip install -r requirements.txt`
7. To start the web server run `python manage.py runserver`
	- Note: you may be asked to perform migrations, run `python manage.py makemigrations && python manage.py migrate`
	- The first time the application is run, run `./manage.py create_groups` to create permissions groups
8. Install the needed packages with `pip install 'prospector==1.3.1' 'bandit==1.7.0'`

### VSCode Remote Container instructions
This method requires that you already have VSCode set up with the VSCode Remote Container extension with a local Docker installation
1. Open repository in VSCode
2. Open command palette (usually CTRL-SHIFT-P), and select "re-open in container"

### Test Instructions
1. Run tests:
- unit tests: `python manage.py test`	
- linter: `prospector`
- Statis analysis: `bandit -r .`

[Development Notes](Documentation/DEVNOTES.md)
