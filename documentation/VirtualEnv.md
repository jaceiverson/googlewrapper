## Create virtual enviornment
I recommended to create a virtualenv using the <a href="https://pypi.org/project/virtualenv/" target="_blank">virtualenv library</a>. Follow these steps:

### install the package to main python instance
```
pip3 install virtualenv
```
### actually create the virtual enviornment
```
python3 -m virtualenv venv
```
### activate the enviornment
```
source venv/bin/activate
```

### general use for virtual environments
It is recommended to use virtualenvs when working with python and storing all your dependencies in a `requirements.txt` file. When you do that, you can simply install all the necessary packages by running the command
```
pip install requirements.txt -r
```
This will attempt to install everything in that text file. Normally packages will include dependency installs automatically. For example, when you run `pip install googlewrapper` all the dependencies (and unfortuneately there are quite a few) will automatically be installed. 
