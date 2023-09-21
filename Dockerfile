# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Copy the dependencies file to the working directory
COPY requirements.txt /docker-test/requirements.txt

# Set the working directory in the container
WORKDIR /docker-test

# Install any dependencies
RUN apk update && apk --no-cache --update add libffi-dev 
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /docker-test

# Specify the command to run on container start
CMD [ "flask" , "run" , "--host=0.0.0.0"]