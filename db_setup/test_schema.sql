USE plants;
GO

DROP TABLE if exists s_beta.watering_test, s_beta.duty_test, s_beta.recording_test, s_beta.botanist_test, s_beta.plant_test, s_beta.location_test;
GO

CREATE TABLE s_beta.recording_test (
    "id" INT IDENTITY(1,1),
    "plant_id" INT NOT NULL,
    "soil_moisture" FLOAT NOT NULL,
    "temperature" FLOAT NOT NULL,
    "datetime" datetime2 NOT NULL
);
GO

ALTER TABLE
 s_beta.recording_test ADD CONSTRAINT "recording_test_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.plant_test (
    "id" INT IDENTITY(0,1),
    "name" VARCHAR(255),
    "scientific_name" VARCHAR(255),
    "location_id" INT
);
GO

ALTER TABLE
    s_beta.plant_test ADD CONSTRAINT "plant_test_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.watering_test(
    "id" INT IDENTITY(1,1),
    "plant_id" INT NOT NULL,
    "datetime" datetime2 NOT NULL
);
GO

ALTER TABLE
    s_beta.watering_test ADD CONSTRAINT "watering_test_id_primary" PRIMARY KEY("id");
GO


CREATE TABLE s_beta.botanist_test (
    "id" INT IDENTITY(1,1),
    "email" VARCHAR(350) NOT NULL,
    "firstname" VARCHAR(100) NOT NULL,
    "lastname" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(30) NOT NULL
);
GO

ALTER TABLE
    s_beta.botanist_test ADD CONSTRAINT "botanist_test_id_primary" PRIMARY KEY("id");
GO

BEGIN TRANSACTION;
INSERT INTO s_beta.botanist_test ("email", "firstname", "lastname", "phone")
VALUES
('gertrude.jekyll@lnhm.co.uk','Gertrude','Jekyll','001-481-273-3691x127'),
('carl.linnaeus@lnhm.co.uk','Carl','Linnaeus','(146)994-1635x35992'),
('eliza.andrews@lnhm.co.uk','Eliza','Andrews','(846)669-6651x75948')
;
COMMIT;

CREATE TABLE s_beta.location_test (
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
    s_beta.location_test ADD CONSTRAINT "location_test_id_primary" PRIMARY KEY("id");
GO

CREATE TABLE s_beta.duty_test(
    "id" INT IDENTITY(1,1),
    "botanist_id" INT NOT NULL,
    "plant_id" INT NOT NULL,
    "start" datetime2 NOT NULL DEFAULT(GETDATE()),
    "end" datetime2
);
GO

ALTER TABLE
    s_beta.duty_test ADD CONSTRAINT "duty_test_id_primary" PRIMARY KEY("id");
GO

ALTER TABLE
 s_beta.recording_test  ADD CONSTRAINT "recording_test_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant_test("id");
GO

ALTER TABLE
    s_beta.plant_test ADD CONSTRAINT "plant_test_location_id_foreign" FOREIGN KEY("location_id") REFERENCES s_beta.location_test("id");
GO

ALTER TABLE
    s_beta.watering_test ADD CONSTRAINT "watering_test_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant_test("id");
GO

ALTER TABLE
    s_beta.duty_test ADD CONSTRAINT "duty_test_plant_id_foreign" FOREIGN KEY("plant_id") REFERENCES s_beta.plant_test("id");
GO

ALTER TABLE
    s_beta.duty_test ADD CONSTRAINT "duty_test_botanist_id_foreign" FOREIGN KEY("botanist_id") REFERENCES s_beta.botanist_test("id");