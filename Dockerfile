FROM python:3
RUN mkdir /code
WORKDIR /code/
COPY . /code/
RUN pip install -r requirements.txt
ENV PORT=8000
EXPOSE $PORT
CMD gunicorn proj1.wsgi:application --bind 0.0.0.0:$PORT
