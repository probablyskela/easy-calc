# easy-calc  
Web platform for publishing custom calculators.
# OLEH SKIP WORST CONTRIBUTOR SO FAR @olegskip
# ONLY FOR LINUX, must have pipenv installed  
To install project: 
In terminal:  
~~~bash  
git clone https://github.com/probablyskela/easy-calc.git
~~~  
~~~bash  
cd easy-calc
~~~
~~~bash  
pipenv install
~~~  
~~~bash  
pipenv shell
~~~bash  
gunicorn -w 2 -b 0.0.0.0:5000 app:app
~~~  
In web-browser:  
go to http://127.0.0.1:8000/api/v1/hello-world-4  

