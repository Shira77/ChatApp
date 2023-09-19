# set base image (host OS)
FROM python:3.8-slim
# set the working directory in the container
RUN update-ca-certificates

WORKDIR /code
# copy the dependencies file to the working directory
COPY requirements.txt .

VOLUME my-volume:/code

# install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --no-cache-dir
# copy the content of the local src directory to the working directory
COPY . .

ENV FLASK_ENV development
# command to run on container start
CMD [ "python", "./chatApp.py" ]