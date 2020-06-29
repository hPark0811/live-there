CREATE TABLE IF NOT EXISTS University (
	id 							INT PRIMARY KEY,
    universityName 				VARCHAR(255),
    campus 						VARCHAR(255),
    institutionType 			CHAR(1),
    postalCode 					CHAR(6),
    city						VARCHAR(255),
    province 					VARCHAR(255),
    CONSTRAINT CHK_institutionType CHECK(institutionType = 'C' OR institutionType = 'U')
);

CREATE TABLE IF NOT EXISTS Rental (
	id 							INT PRIMARY KEY,
    rentalPrice					SMALLINT,
    postalCode 					CHAR(6),
    longitude					DECIMAL(9,7),
    latitude					DECIMAL(9,7),
    stubId 						INT,
    bathroomCount				TINYINT,
    bedroomCount				TINYINT,
    lastUpdatedDate 			DATE,
    CONSTRAINT CHK_bathroomCount CHECK(bathroomCount > 0),
    CONSTRAINT CHK_bedroomCount CHECK(bathroomCount > 0)
);

CREATE TABLE IF NOT EXISTS RentalRange (
	universityId 				INT,
    rentalId					INT,
    rentToUniversityDistance 	DECIMAL(3, 1),
    PRIMARY KEY (universityId, rentalId),
    FOREIGN KEY (universityId) REFERENCES University(id),
    FOREIGN KEY (rentalId) REFERENCES Rental(id)
);