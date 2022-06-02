# Take the ubuntu/apache2 container
FROM ubuntu/apache2:latest

#Add a label
#LABEL maintainer="kronos443@mitchell.click"

# Define a Docker build version
ENV DOCKER_BUILD_VERSION=V0.0.1

# Install needed apps
RUN apt-get update
RUN apt-get install python3 python3-pip python-dev -y
# Add optional items for debug
RUN apt-get install nano -y

# Install Python libs
RUN pip install nut2 matplotlib

# Add the app files
#RUN mkdir -p /config/logs
#RUN mkdir -p /config/certs
#RUN mkdir -p /config/db
#COPY ./config /config
WORKDIR /app
COPY ./app /app

# Set the CGI to start
RUN a2enmod cgid

# Configure apache2 for CGI
RUN mkdir /var/www/cgi-bin
RUN cat ./apache2.conf >> /etc/apache2/apache2.conf
RUN mv ./serve-cgi-bin.conf /etc/apache2/conf-available
RUN mv /var/www/html/index.html /var/www/html/apache2.html
RUN mv ./apache2-foreground /usr/bin/apache2-foreground
RUN chmod +x ./set_config.sh
RUN chmod +x /usr/bin/apache2-foreground

# Setup the app files 
RUN mv ./cgi_test.py /var/www/cgi-bin
RUN chmod +x /var/www/cgi-bin/cgi_test.py
RUN mv ./ups_display.html /var/www/html/index.html
RUN mv ./ups_display.py /var/www/cgi-bin

RUN mv ./graphics /var/www/html
RUN mv ./bootstrap /var/www/html
RUN mv ./fontawesome /var/www/html
RUN mv ./jquery /var/www/html

ENV PYTHONPATH=/app

#RUN pip install --no-cache-dir -r requirements.txt
