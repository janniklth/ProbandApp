CREATE TABLE IF NOT EXISTS Medication (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Proband (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    gender ENUM('M', 'F', 'D') NOT NULL,
    birthday DATE NOT NULL,
    weight DOUBLE(8, 2) NOT NULL,
    height DOUBLE(8, 2) NOT NULL,
    health FLOAT,
    countryid BIGINT NOT NULL,
    isactive BOOLEAN DEFAULT true
);
CREATE TABLE IF NOT EXISTS ProbandMedication (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    probandid BIGINT NOT NULL,
    medicationid BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS Sickness (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Country(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    countrycode varchar(3) NOT NULL,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS ProbandSickness(
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    probandid BIGINT NOT NULL,
    sicknessid BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Gender(
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50)
);


ALTER TABLE ProbandMedication
    -- ADD CONSTRAINT `patientmedication_proband_id_fk`
        ADD FOREIGN KEY (`probandid`) REFERENCES Proband(`id`);

ALTER TABLE
    ProbandSickness
    -- ADD CONSTRAINT `patientsickness_patientid_fk`
        ADD FOREIGN KEY (`probandid`) REFERENCES Proband(`id`);
ALTER TABLE
    ProbandMedication
    -- ADD CONSTRAINT `patientmedication_medicationid_fk`
        ADD FOREIGN KEY(`medicationid`) REFERENCES `Medication`(`id`);
ALTER TABLE
    Proband
    -- ADD CONSTRAINT `patient_countryid_fk`
        ADD FOREIGN KEY (`countryid`) REFERENCES `Country`(`id`);
ALTER TABLE
    ProbandSickness
    -- ADD CONSTRAINT `patientsickness_sicknessid_fk_2`
        ADD FOREIGN KEY (`sicknessid`) REFERENCES `Sickness`(`id`);

SET GLOBAL FOREIGN_KEY_CHECKS=0;