CREATE USER postgres WITH PASSWORD 'postgres';

CREATE DATABASE cinema_project_db;
GRANT ALL PRIVILEGES ON DATABASE cinema_project_db TO postgres;