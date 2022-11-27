echo 'sqlite:///test.db' > config.txt
coverage run --source=app -m unittest discover && coverage report -m