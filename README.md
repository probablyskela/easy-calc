# easy-calc
Web platform for publishing custom calculators.
To install project: 
# ONLY FOR LINUX, need to have pipenv installed
In terminal:
$ git clone https://github.com/probablyskela/easy-calc.git
$ cd easy-calc
$ pipenv install
$ pipenv shell
$ gunicorn -w 2 hello:app
In web-browser:
go to http://127.0.0.1:8000/api/v1/hello-world-4
