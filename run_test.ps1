'sqlite:///test.db' | Out-File -FilePath .\config.txt
coverage run --source=app -m unittest discover ; if ($?) { coverage report -m }