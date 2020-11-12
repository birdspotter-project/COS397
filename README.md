# BirdSpotter
BirdSpotter is a graphical interface for integrating and viewing machine learning and field survey data for rapid population estimation of colonial nesting birds

### Development Instructions
1. Clone repo into desired directory using `git clone`
2. Move into the `COS397/birdspotter` directory
3. It is recommended to create a virtual environment for development
	- For installation instructions view this [page](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
4. Once in the desired environment install required packages by running `pip install -r requirements.txt`
5. To start the web server run `python manage.py runserver`
	- Note: you may be asked to perform migrations, run `python manage.py makemigrations`
