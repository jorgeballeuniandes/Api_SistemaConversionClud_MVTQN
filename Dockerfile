FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y python3.9

RUN apt-get install -y pip

RUN apt-get install redis-server -y

RUN apt-get install ffmpeg  -y

RUN redis-server & 

# copy the requirements file into the image
COPY "." "/home/app" 

# switch working directory
WORKDIR /home/app

RUN pip install --upgrade pip



RUN pip install -r requirements.txt


# configure the container to run in an executed manner

CMD ["python3", "app.py" ]