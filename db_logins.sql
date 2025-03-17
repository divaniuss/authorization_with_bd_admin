CREATE DATABASE db_logins;
USE db_logins;

CREATE TABLE [Clients]
(
    [ID] INT IDENTITY,
    [login] VARCHAR(50) NOT NULL UNIQUE,
    [Password] VARCHAR(50) NOT NULL,
);

SELECT * FROM [Clients]

USE db_name;