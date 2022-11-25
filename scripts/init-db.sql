CREATE DATABASE `flask`;

use flask;

CREATE TABLE badTranslations (
FROMTAG varchar(2) not null,
TOTAG varchar(2) not null,
FROM_TEXT varchar(60) not null,
TO_TEXT varchar(60) not null,
ID integer(30) not null,
COMPLAINTS integer(5) not null,
PRIMARY KEY (ID)
);

CREATE TABLE possibleBetterTranslations (
FROM_TEXT varchar(60) not null,
TO_TEXT varchar(60) not null,
SECONDID integer(30) not null,
FID integer(30) not null,
VOTES integer(5) not null,
TIMESTAMP timestamp not null,
FOREIGN KEY (FID) REFERENCES badTranslations(ID),
PRIMARY KEY (SECONDID)
);