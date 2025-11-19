#!/bin/zsh
docker run --rm -p 8080:80 \
  -v "$(pwd)/demo":/var/www/html \
  -v "$(pwd)/php.ini":/usr/local/etc/php/php.ini \
  php:8.2-apache
