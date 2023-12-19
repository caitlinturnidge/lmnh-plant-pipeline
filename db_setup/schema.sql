USE plants;
GO

DROP TABLE if exists s_beta.watering, s_beta.duty, s_beta.recording, s_beta.botanist, s_beta.plant, s_beta.location;
GO

CREATE TABLE s_beta.recording (
    "id" INT IDENTITY(1,1),
    "plant_id" INT NOT NULL,
    "soil_moisture" FLOAT NOT NULL,
    "temperature" FLOAT NOT NULL,
    "datetime" datetimeoffset NOT NULL
);
GO

ALTER TABLE
 s_beta.recording ADD CONSTRAINT "recording_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.plant(
    "id" INT IDENTITY(0,1),
    "name" VARCHAR(255) NOT NULL,
    "scientific_name" VARCHAR(255) NOT NULL,
    "location_id" INT
);
GO

ALTER TABLE
    s_beta.plant ADD CONSTRAINT "plant_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.watering(
    "id" INT IDENTITY(1,1),
    "plant_id" INT NOT NULL,
    "datetime" datetimeoffset NOT NULL
);
GO

ALTER TABLE
    s_beta.watering ADD CONSTRAINT "watering_id_primary" PRIMARY KEY("id");
GO


CREATE TABLE s_beta.botanist(
    "id" INT IDENTITY(1,1),
    "email" VARCHAR(350) NOT NULL,
    "firstname" VARCHAR(100) NOT NULL,
    "lastname" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(30) NOT NULL
);
GO

ALTER TABLE
    s_beta.botanist ADD CONSTRAINT "botanist_id_primary" PRIMARY KEY("id");
GO

BEGIN TRANSACTION;
INSERT INTO s_beta.botanist ("email", "firstname", "lastname", "phone")
VALUES
('gertrude.jekyll@lnhm.co.uk','Gertrude','Jekyll','001-481-273-3691x127'),
('carl.linnaeus@lnhm.co.uk','Carl','Linnaeus','(146)994-1635x35992'),
('eliza.andrews@lnhm.co.uk','Eliza','Andrews','(846)669-6651x75948')
;
COMMIT;

CREATE TABLE s_beta.location(
    "id" INT IDENTITY(1,1),
    "latitude" FLOAT NOT NULL,
    "longitude" FLOAT NOT NULL,
    "town" VARCHAR(100) NOT NULL,
    "city" VARCHAR(100) NOT NULL,
    "country_code" NCHAR(2) NOT NULL,
    "continent" VARCHAR(50) NOT NULL
);
GO

ALTER TABLE
    s_beta.location ADD CONSTRAINT "location_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.duty(
    "id" INT IDENTITY(1,1),
    "botanist_id" INT NOT NULL,
    "plant_id" INT NOT NULL
);
GO

ALTER TABLE
    s_beta.duty ADD CONSTRAINT "duty_id_primary" PRIMARY KEY("id");
GO

ALTER TABLE
 s_beta.recording  ADD CONSTRAINT "recording_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant("id");
GO

ALTER TABLE
    s_beta.plant ADD CONSTRAINT "plant_location_id_foreign" FOREIGN KEY("location_id") REFERENCES s_beta.location("id");
GO

ALTER TABLE
    s_beta.watering ADD CONSTRAINT "watering_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant("id");
GO

ALTER TABLE
    s_beta.duty ADD CONSTRAINT "duty_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant("id");
GO

ALTER TABLE
    s_beta.duty ADD CONSTRAINT "duty_botanist_id_foreign" FOREIGN KEY("botanist_id") REFERENCES s_beta.botanist("id");