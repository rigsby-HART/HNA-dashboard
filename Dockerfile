FROM     python:3.11
WORKDIR  /app
COPY    .	/app
RUN     pip install --upgrade pip --no-cache-dir
RUN		pip install -r /app/requirements.txt --no-cache-dir
EXPOSE  8050
EXPOSE  8000
CMD		["gunicorn","app:server"]
