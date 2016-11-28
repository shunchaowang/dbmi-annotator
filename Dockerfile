############################ DBMI-ANNOTATOR ############################
FROM ubuntu:14.04
MAINTAINER Yifan Ning "yin2@pitt.edu"

# build image from nodejs server
# FROM node:0.12.17

RUN apt-get update
RUN apt-get install -y nodejs npm python-pip libpq-dev python-dev emacs

RUN update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

# Create dbmi-annotator directory
RUN mkdir -p /home/yin2/dbmi-annotator
WORKDIR /home/yin2/dbmi-annotator

# Install dependencies
COPY package.json /home/yin2/dbmi-annotator/
RUN npm install

# Bundle dbmi-annotator source
COPY . /home/yin2/dbmi-annotator

# Use Production mode configuration
COPY config/production.conf /home/yin2/dbmi-annotator/config/config.js

RUN ./node_modules/.bin/browserify config/production-app.js -o /home/yin2/dbmi-annotator/public/dbmiannotator/js/app.bundle.js


# Install dependencies for annotation pre-load program
RUN pip install psycopg2 elasticsearch

# # Load SPLs annotation to database mpevidence 
# WORKDIR /home/yin2/dbmi-annotator/translation/csv-data-loader
# CMD [ "python", "loadDomeoAnnsToRDB.py"]

# # Query database mpevidence and load into elasticsearch 
# WORKDIR /home/yin2/dbmi-annotator/translation/rdb-data-loader
# CMD [ "python", "load-rdb-annotations.py"]

# Start nodejs server
# WORKDIR /home/yin2/dbmi-annotator
EXPOSE 3000
CMD [ "npm", "start" ]