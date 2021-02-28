\set birdspotter_password `echo \'$DBPASSWORD\'`
\set birdspotter_dbname `echo $DBNAME`
\set birdspotter_user `echo $DBUSERNAME`
CREATE DATABASE :birdspotter_dbname;
CREATE USER :birdspotter_user WITH PASSWORD :birdspotter_password;
GRANT ALL PRIVILEGES ON DATABASE :birdspotter_dbname TO :birdspotter_user;