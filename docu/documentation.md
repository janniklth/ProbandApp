# Database Documentation

## Entity-Relationship-Model

The following diagram shows the entity-relationship-model of the database.

![Entity-Relationship-Model](erm.jpeg)



## Schema

Medication (__id__: bigint, name: varchar(255)), 

Gender (__id__: bigint, name: varchar(255)), 

Country (__id__: bigint, name: varchar(255), countrycode: varchar(255)), 

Disease (__id__: bigint, name: varchar(255)), 

Proband (__id__: bigint, first_name: varchar(255), last_name: varchar(255), email: varchar(255), gender_id: bigint, birthday: date, weight: double(8, 2), height: double(8, 2), health: float, bmi: double(8, 2), country_id: bigint, is_active: boolean, last_changed: datetime), FK: country_id references Country, gender_id references Gender

ProbandMedication (__id__: bigint, proband_id: bigint, medication_id: bigint), FK: proband_id references Proband, medication_id references Medication

ProbandDiseases (__id__: bigint, proband_id: bigint, sickness_id: bigint), FK: proband_id references Proband, sickness_id references Disease
