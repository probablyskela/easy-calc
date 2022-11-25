'postgresql+pg8000://postgres:123456@localhost:5432/postgres' | Out-File -FilePath .\config.txt
python wsgi.py