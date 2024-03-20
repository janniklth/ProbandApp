USE dbproject;

CREATE SCHEMA IF NOT EXISTS dbproject;

CREATE TABLE IF NOT EXISTS MEDICATION (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS PROBAND (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    genderId BIGINT NOT NULL,
    birthday DATE NOT NULL,
    weight DOUBLE(8, 2) NOT NULL,
    height DOUBLE(8, 2) NOT NULL,
    health FLOAT,
    countryId BIGINT NOT NULL,
    isActive BOOLEAN DEFAULT true,
    lastChanged TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS PROBANDMEDICATION (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    probandId BIGINT NOT NULL,
    medicationId BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS SICKNESS (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS COUNTRY (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    countrycode varchar(3) NOT NULL,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS PROBANDSICKNESS(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    probandId BIGINT NOT NULL,
    sicknessId BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS GENDER(
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50)
);


ALTER TABLE PROBANDMEDICATION
    -- ADD CONSTRAINT `patientmedication_proband_id_fk`
        ADD FOREIGN KEY (`probandId`) REFERENCES PROBAND(`id`);

ALTER TABLE
    PROBANDSICKNESS
    -- ADD CONSTRAINT `patientsickness_patientid_fk`
        ADD FOREIGN KEY (`probandId`) REFERENCES PROBAND(`id`);
ALTER TABLE
    PROBANDMEDICATION
    -- ADD CONSTRAINT `patientmedication_medicationid_fk`
        ADD FOREIGN KEY(`medicationId`) REFERENCES `MEDICATION`(`id`);
ALTER TABLE
    PROBAND
    -- ADD CONSTRAINT `patient_countryid_fk`
        ADD FOREIGN KEY (`countryId`) REFERENCES `COUNTRY`(`id`);
ALTER TABLE
    PROBAND
    -- ADD CONSTRAINT `patient_countryid_fk`
        ADD FOREIGN KEY (`genderId`) REFERENCES `GENDER`(`id`);
ALTER TABLE
    PROBANDSICKNESS
    -- ADD CONSTRAINT `patientsickness_sicknessid_fk_2`
        ADD FOREIGN KEY (`sicknessId`) REFERENCES `SICKNESS`(`id`);

SET GLOBAL FOREIGN_KEY_CHECKS=0;