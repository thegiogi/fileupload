DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS FILES;
DROP TABLE IF EXISTS LINES;

CREATE TABLE USER
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE FILES
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  USER_ID INTEGER NOT NULL,
  FILENAME TEXT NOT NULL,
  TIME_UPLOADED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  TAG TEXT,
  LINES INT,
  VALID INT,
  FOREIGN KEY (USER_ID) REFERENCES USER (ID)
);

CREATE TABLE LINES
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  FILE_ID INTEGER NOT NULL,
  LINE_NR INTEGER NOT NULL,
  BODY TEXT,
  FOREIGN KEY (FILE_ID) REFERENCES FILES (ID) ON DELETE CASCADE
);
