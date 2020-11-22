CREATE DATABASE codes_images;
CREATE USER heroku WITH password 'herokuneverguess123';
GRANT ALL ON DATABASE codes_images TO heroku;

CREATE SEQUENCE image_ids;
CREATE TABLE codes (
  id INTEGER PRIMARY KEY DEFAULT NEXTVAL('image_ids'),
  code CHAR(64),
  image BYTEA(10000));