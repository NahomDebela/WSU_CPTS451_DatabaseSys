CREATE TABLE Business (
	business_id CHAR(22) PRIMARY KEY,
	name VARCHAR(75) NOT NULL,
	city VARCHAR(20) NOT NULL,
	state CHAR(2) NOT NULL,
	postal_code CHAR(5) NOT NULL,
	address VARCHAR(100) NOT NULL,
	is_open INTEGER CHECK (is_open = 0 OR is_open = 1) NOT NULL,
	numCheckins INTEGER NOT NULL,
	numTips INTEGER NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	stars FLOAT CHECK (stars <= 5 AND stars >= 0) NOT NULL,
	review_count INTEGER NOT NULL
);

CREATE TABLE Categories (
	business_id VARCHAR(22),
	category_name VARCHAR(50),
	PRIMARY KEY (category_name, business_id),
	FOREIGN KEY (business_id) REFERENCES Business (business_id)
);

CREATE TABLE Checkin (
	business_id VARCHAR(22),
	date VARCHAR(20),
	PRIMARY KEY (date, business_id),
	FOREIGN KEY (business_id) REFERENCES Business (business_id)
);

CREATE TABLE Users (
	user_id	CHAR(22) PRIMARY KEY,
	totalLikes INTEGER,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	yelping_since DATE NOT NULL,
	name VARCHAR(50) NOT NULL,
	tip_count INTEGER,
	average_stars FLOAT CHECK (average_stars <= 5.0 AND average_stars >= 0.0),
	useful INTEGER,
	funny INTEGER,
	cool INTEGER,
	fans INTEGER
);

CREATE TABLE Friend (
    user_id CHAR(22),
    friend_id CHAR(22),
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (friend_id) REFERENCES Users (user_id)
);

CREATE TABLE Tip (
	business_id CHAR(22) NOT NULL,
	date DATE NOT NULL,
	likes INTEGER,
	text VARCHAR(5000) NOT NULL,
	user_id	CHAR(22) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES Users (user_id),
	FOREIGN KEY (business_id) REFERENCES Business (business_id)
);


