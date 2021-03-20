FROM postgres:12

ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB testdb 
COPY init.sql /docker-entrypoint-initdb.d/