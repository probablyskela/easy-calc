echo 'postgresql+pg8000://postgres:123@localhost:5432/postgres' > config.txt
gunicorn -w 2 -b 0.0.0.0:5000 app:app