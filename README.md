# BirdSpotter
BirdSpotter is a graphical interface for integrating and viewing machine learning and field survey data for rapid population estimation of colonial nesting birds. The creation of this interface will allow officials to quickly and effectively draw conclusions based on data provided from human and machine learning observations of bird species, activity, and location. 

### Deliverables
- [Software Requirements Specification](Documentation/Deliverables/Software_Requirements_Specification/SRS.pdf)
- [Software Design Document](Documentation/Deliverables/Software_Design_Document/SDD.pdf)
- [UI Design Document](Documentation/Deliverables/UI_Design_Document/UIDD.pdf)
- [Critical Design Review](https://github.com/devinchristianson/COS397/blob/master/Documentation/Deliverables/CDR.pdf)

### Development Instructions
1. Clone repo into desired directory using `git clone`
2. Move into the `COS397/birdspotter` directory
3. It is recommended to create a virtual environment for development
	- For installation instructions view this [page](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
4. Install miniconda (https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
5. Install GDAL: `conda install gdal`
6. Correct dependencies: `conda update numpy`
5. Once in the desired environment install required packages by running `pip install -r requirements.txt`
6. To start the web server run `python manage.py runserver`
	- Note: you may be asked to perform migrations, run `python manage.py makemigrations && python manage.py migrate`

[Development Notes](Documentation/DEVNOTES.md)
