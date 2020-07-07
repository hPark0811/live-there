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
	universityId				INT PRIMARY KEY,
    FOREIGN KEY (universityId) REFERENCES University(id)
)