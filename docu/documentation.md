# Database Documentation

## Entity-Relationship-Model

The following diagram shows the entity-relationship-model of the database.

![Entity-Relationship-Model](images/er-model.png)



## Schema

Medication (__ID__: bigint, Name: varchar(255)), 

Gender (__ID__: bigint, Name: varchar(255)), 

Country (__ID__: bigint, Name: varchar(255), CountryCode: varchar(255)), 

Disease (__ID__: bigint, Name: varchar(255)), 

Proband (__ID__: bigint, FirstName: varchar(255), LastName: varchar(255), Email: varchar(255), GenderId: bigint, Birthday: date, Weight: double(8, 2), Height: double(8, 2), CountryId: bigint, IsActive: tinyint(1), LastChanged: datetime), FK: CountryId references Country, GenderId references Gender

ProbandMedication (__ID__: bigint, ProbandId: bigint, MedicationId: bigint), FK: ProbandId references Proband, MedicationId references Medication

ProbandDiseases (__ID__: bigint, ProbandId: bigint, SicknessId: bigint), FK: ProbandId references Proband, SicknessId references Disease
