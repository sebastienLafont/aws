FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=entreprise

COPY init.sql /docker-entrypoint-initdb.d/
