CREATE TABLE IF NOT EXISTS University (
	id 							INT PRIMARY KEY AUTO_INCREMENT,
    universityName 				VARCHAR(255) NOT NULL,
    campus 						VARCHAR(255) NOT NULL,
    institutionType 			CHAR(1) NOT NULL,
    postalCode 					CHAR(6) NOT NULL,
    city						VARCHAR(255) NOT NULL,
    province 					VARCHAR(255) NOT NULL,
    CONSTRAINT CHK_institutionType CHECK(institutionType = 'C' OR institutionType = 'U'),
    UNIQUE KEY (universityName, campus)
);

CREATE TABLE IF NOT EXISTS Rental (
	id 							INT PRIMARY KEY AUTO_INCREMENT,
    rentalPrice					SMALLINT NOT NULL,
    postalCode 					CHAR(6) NOT NULL,
    longitude					DECIMAL(9,7) NOT NULL,
    latitude					DECIMAL(9,7) NOT NULL,
    stubId 						INT,
    bathroomCount				TINYINT,
    bedroomCount				TINYINT,
    lastUpdatedDate 			DATE NOT NULL,
    propertyType                VARCHAR(255),
    CONSTRAINT CHK_bathroomCount CHECK(bathroomCount > 0),
    CONSTRAINT CHK_bedroomCount CHECK(bathroomCount > 0),
    UNIQUE KEY (stubId)
);

CREATE TABLE IF NOT EXISTS RentalRange (
	universityId 				INT,
    rentalId					INT,
    rentToUniversityDistance 	DECIMAL(3, 1) NOT NULL,
    PRIMARY KEY (universityId, rentalId),
    FOREIGN KEY (universityId) REFERENCES University(id),
    FOREIGN KEY (rentalId) REFERENCES Rental(id)
);

CREATE TABLE IF NOT EXISTS MainCampusMap (
    universityId    INT PRIMARY KEY,
    FOREIGN KEY (universityId) REFERENCES University(id)
);


CREATE TABLE IF NOT EXISTS YelpSchema (
    yelpId				INT PRIMARY KEY,
    priceLevel          INT NOT NULL,
    minPrice            float,
    maxPrice            float
);

CREATE TABLE IF NOT EXISTS Restaurant (
    restaurantId 				INT PRIMARY KEY AUTO_INCREMENT,
    restaurantType				CHAR(1),
    postalCode 					CHAR(6) NOT NULL,
    yelpId              		INT NOT NULL,
    FOREIGN KEY (yelpId) REFERENCES YelpSchema()
);

CREATE TABLE IF NOT EXISTS RestaurantRange (
    universityId 					INT,
    restaurantId					INT,
    restaurantToUniversityDistance 	DECIMAL(3, 1) NOT NULL,
    PRIMARY KEY (universityId, restaurantId),
    FOREIGN KEY (universityId) REFERENCES University(id),
    FOREIGN KEY (restaurantId) REFERENCES Restaurant(restaurantId)
);

CREATE TABLE IF NOT EXISTS AverageUtilityFee (
    universityId INT PRIMARY KEY NOT NULL,
    averageEC FLOAT,
    averageNG FLOAT,
    averageHD FlOAT,
	FOREIGN KEY (universityId) REFERENCES University(id)
);