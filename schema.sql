--Creation of the user table.
CREATE TABLE "users" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	username TEXT(25) NOT NULL UNIQUE,
	password TEXT(80) NOT NULL,
	firstname TEXT(25) NOT NULL,
	name TEXT(25) NOT NULL
);

--Creation of the tasks table.
CREATE TABLE "tasks" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT(30) NOT NULL,
	description TEXT(256) NOT NULL,
    status INTEGER NOT NULL DEFAULT(0),
    owner INTEGER NOT NULL,
    CONSTRAINT Tasks_FK FOREIGN KEY (owner) REFERENCES users(id)
);