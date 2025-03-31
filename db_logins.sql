CREATE DATABASE db_logins;
USE db_logins;

CREATE TABLE [Clients]
(
    [ID] INT IDENTITY,
	[Time_log] VARCHAR(50),
    [login] VARCHAR(50) NOT NULL UNIQUE,
    [Password] VARCHAR(255) NOT NULL,
);



SELECT * FROM [Clients]
DROP TABLE [Clients]