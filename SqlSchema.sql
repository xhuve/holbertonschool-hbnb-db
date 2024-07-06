CREATE TABLE amenities (
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NULL,
    place_id VARCHAR(60) NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id)
);

CREATE TABLE cities (
    name VARCHAR NOT NULL,
    population INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (country_id) REFERENCES countries (id)
);

CREATE TABLE countries (
    name VARCHAR NOT NULL,
    population INTEGER NOT NULL,
    code VARCHAR NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id)
);

CREATE TABLE places (
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NULL,
    address VARCHAR(256) NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    price_per_night FLOAT NOT NULL,
    number_of_rooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    max_guests INTEGER NOT NULL,
    amenity_id INTEGER NULL,
    city_id INTEGER NULL,
    host_id INTEGER NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (amenity_id) REFERENCES amenities (id),
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (host_id) REFERENCES users (id)
);

CREATE TABLE reviews (
    feedback VARCHAR NOT NULL,
    rating VARCHAR NOT NULL,
    comment VARCHAR NULL,
    place_id INTEGER NULL,
    user_id INTEGER NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);


CREATE TABLE users (
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NULL,
    city_id INTEGER NULL,
    is_admin BOOLEAN NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NULL,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (city_id) REFERENCES cities (id)
);