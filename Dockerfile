# Use an official Python runtime as a parent image
FROM python:3.11-slim

# set working directory to /app
WORKDIR /app

# copy current directory contents into the container at /app
COPY . /app

# install packages needed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# env variable
ENV FLASK_APP=hello.py
EXPOSE 5000

# run flask when container launches
CMD ["flask", "run", "--host=0.0.0.0"]