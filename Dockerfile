FROM ubuntu:precise

MAINTAINER Bruno Gola "brunogola@gmail.com"

RUN echo "deb http://archive.ubuntu.com/ubuntu/ precise universe" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install net-tools lynx nano wget
RUN apt-get -y install python-software-properties
RUN add-apt-repository -y ppa:nginx/stable
RUN add-apt-repository -y ppa:ondrej/php5-oldstable
RUN apt-get update

RUN apt-get -y install nginx php5-fpm php5-mysql php-apc php5-imagick php5-imap php5-mcrypt

ADD ./default /etc/nginx/sites-available/ 
RUN echo "cgi.fix_pathinfo = 0;" >> /etc/php5/fpm/php.ini
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir /var/www
RUN echo "<?php phpinfo(); ?>" > /var/www/phpinfo.php

EXPOSE 80

CMD service php5-fpm start && nginx
