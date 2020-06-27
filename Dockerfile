FROM python:3.8
RUN apt-get update
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]