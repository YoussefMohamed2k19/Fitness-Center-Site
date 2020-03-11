CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    mobile_number VARCHAR (50) NOT NULL,
    weight integer NOT NULL,
    height integer NOT NULL,
    age integer NOT NULL,
    exercise integer NOT NULL,
    gender text NOT NULL,
    area text NOT NULL
);

CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    email VARCHAR NOT NULL,
    message text NOT NULL
);