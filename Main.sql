--CREATING TABLES--

-- Creating alien --
CREATE TABLE alien (
alien_id SERIAL PRIMARY KEY,
name varchar(50) NOT NULL,
surname varchar(50) NOT NULL,
url varchar(100) default '/static/images/person.png'
);

-- Creating person --
CREATE TABLE person (
person_id SERIAL PRIMARY KEY,
name varchar(50) NOT NULL,
surname varchar(50) NOT NULL,
url varchar(100) default '/static/images/alien.png'
);

-- Creating ship --
CREATE TABLE ship (
ship_id SERIAL PRIMARY KEY);

-- Create personShip --
CREATE TABLE personShip (
person_id INT NOT NULL,
ship_id INT NOT NULL,
start_time TIMESTAMP,
finish_time TIMESTAMP,
FOREIGN KEY (ship_id) REFERENCES ship (ship_id),
FOREIGN KEY (person_id) REFERENCES person (person_id),
CHECK (finish_time > start_time)
);

-- Create Experiment --
CREATE TABLE experiment (
experiment_id SERIAL PRIMARY KEY,
person_id INT NOT NULL,
ship_id INT NOT NULL,
time TIMESTAMP,
FOREIGN KEY (person_id) REFERENCES person (person_id),
FOREIGN KEY (ship_id) REFERENCES ship (ship_id)
);

-- Create ExperimentAlien --
CREATE TABLE experimentAlien (
experiment_id INT NOT NULL,
alien_id INT NOT NULL,
FOREIGN KEY (experiment_id) REFERENCES experiment (experiment_id),
FOREIGN KEY (alien_id) REFERENCES alien (alien_id)
);

-- Create Excursion --
CREATE TABLE excursion (
excursion_id SERIAL PRIMARY KEY,
alien_id INT NOT NULL,
time TIMESTAMP,
FOREIGN KEY (alien_id) REFERENCES alien (alien_id)
);

-- Create ExcursionPerson --
CREATE TABLE excursionPerson (
excursion_id INT NOT NULL,
person_id INT NOT NULL,
FOREIGN KEY (excursion_id) REFERENCES excursion (excursion_id),
FOREIGN KEY (person_id) REFERENCES person (person_id)
);

-- Create kills --
CREATE TABLE kills (
kill_id SERIAL PRIMARY KEY,
person_id INT NOT NULL,
alien_id INT UNIQUE NOT NULL,
time TIMESTAMP,
FOREIGN KEY (alien_id) REFERENCES alien (alien_id),
FOREIGN KEY (person_id) REFERENCES person (person_id)
);

-- Create Transfer --
CREATE TABLE transfer (
transfer_id SERIAL PRIMARY KEY,
person_id INT NOT NULL,
alien_id INT UNIQUE NOT NULL,
ship_to_id INTEGER NOT NULL,
ship_from_id INTEGER NOT NULL,
time TIMESTAMP,
FOREIGN KEY (alien_id) REFERENCES alien (alien_id),
FOREIGN KEY (person_id) REFERENCES person (person_id),
CHECK (ship_to_id <> ship_from_id)
);

-- Create Escape --
CREATE TABLE escape (
escape_id SERIAL PRIMARY KEY,
person_id INT NOT NULL,
ship_id INTEGER NOT NULL,
time TIMESTAMP,
FOREIGN KEY (ship_id) REFERENCES ship (ship_id),
FOREIGN KEY (person_id) REFERENCES person (person_id)
);

-- Create Stolen --
CREATE TABLE stolen (
stolen_id SERIAL PRIMARY KEY,
person_id INT NOT NULL,
alien_id INT NOT NULL,
ship_id INTEGER NOT NULL,
time TIMESTAMP,
FOREIGN KEY (person_id) REFERENCES person (person_id),
FOREIGN KEY (alien_id) REFERENCES alien (alien_id),
FOREIGN KEY (ship_id) REFERENCES ship (ship_id) 
);


--FILLING TABLES--

-- Fill alien --
INSERT INTO alien (alien_id, name, surname) VALUES
	(1, 'Caitian', 'Calamarain'),
	(2, 'Caleban', 'Calcinite'),
	(3, 'Callineans', 'Calvin'),
	(4, 'Caliban', 'Capelons'),
	(5, 'Catnipians', 'Conductoid'), 
	(6, 'Cascan', 'Chaethe'),
	(7, 'Cardassian', 'Carggites'),
	(8, 'Carrionites', 'Cat'),
	(9, 'Cathar', 'Catalyte'),
	(10, 'Cavalier', 'Celareon');

-- Fill person -
INSERT INTO person (person_id, name, surname) VALUES
	(11, 'Ihor', 'Ramskyi'),
	(12, 'Andrew', 'Turko'),
	(13, 'Khrystia', 'Sliusarchuk'),
	(14, 'Bohdan', 'Vey'),
	(15, 'Anna', 'Pashuk'), 
	(16, 'Oleksa', 'Hryniv'),
	(17, 'Stephen', 'King'),
	(18, 'Jane', 'Hawking'),
	(19, 'Albert', 'Einstein'),
	(20, 'Nikola', 'Tesla');

-- Fill ship -
INSERT INTO ship (ship_id) VALUES
	(21), (22), (23), (24), (25), 
	(26), (27), (28), (29), (30);

-- Fill personShip --
INSERT INTO personShip (person_id, ship_id, start_time, finish_time) VALUES
	(11, 21, '2004-10-19 10:23:54', '2004-11-19 10:00:00'),
	(11, 23, '2004-12-19 9:23:54', '2005-12-25 9:00:00'),
	(12, 23, '2004-04-19 10:00:00', '2006-04-19 10:00:00'),
	(13, 23, '2016-10-20 9:23:00', '2017-10-20 9:23:00'),
	(13, 24, '2018-02-01 13:00:00', '2019-12-01 13:30:00'),
	(13, 25, '2020-01-02 17:30:00', '2021-01-02 18:30:00'),
	(14, 24, '2007-03-23 18:20:00', '2009-08-04 20:24:50'),
	(15, 24, '2008-05-04 20:23:50', '2010-06-04 20:00:50'),
	(16, 24, '2009-07-15 01:21:30', '2009-07-20 01:27:30'),
	(17, 27, '2010-06-26 19:23:15', '2012-06-26 19:15:00'),
	(18, 27, '2011-09-07 07:25:00', '2012-01-07 07:26:00'),
	(18, 29, '2012-08-18 08:50:19', '2020-08-18 08:13:19'),
	(19, 29, '2014-11-09 09:20:54', '2014-11-10 09:09:54'),
	(20, 29, '2013-10-19 23:23:50', '2014-11-19 23:03:50');

-- Fill Experiment --
INSERT INTO experiment (experiment_id, person_id, ship_id, time) VALUES
	(31, 11, 21, '2004-10-20 10:23:54'),
	(32, 11, 23, '2003-01-19 9:23:54'),
	(33, 12, 22, '2016-04-01 10:00:00'),
	(34, 13, 23, '2017-02-20 9:23:00'),
	(35, 13, 24, '2018-02-01 15:00:00'),
	(36, 13, 25, '2020-03-02 17:30:00'),
	(37, 14, 24, '2008-03-23 18:20:00'),
	(38, 15, 25, '2010-05-04 20:23:50'),
	(39, 18, 26, '2011-10-08 07:25:00'),
	(40, 17, 27, '2011-07-26 19:23:15');

-- Fill ExperimentAlien --
INSERT INTO experimentAlien (experiment_id, alien_id) VALUES
	(31, 1), (31, 2), (31, 2), (31, 3), (31, 4), (32, 5), 
	(33, 3), (34, 4), (34, 2), (34, 10), (35, 5), (35, 7),
	(36, 6), (36, 8), (37, 7), (37, 10), (37, 3), (38, 8), 
	(39, 9), (40, 10);

-- Fill Excursion --
INSERT INTO excursion (excursion_id, alien_id, time) VALUES
	(41, 1, '2004-10-19 10:23:54'),
	(42, 2, '2004-12-20 9:23:54'),
	(43, 3, '2016-10-21 9:23:00'),
	(44, 4, '2018-02-02 13:00:00'),
	(45, 5, '2020-01-03 17:30:00'),
	(46, 6, '2009-07-16 01:21:30'),
	(47, 7, '2011-09-08 07:25:00'),
	(48, 8, '2014-11-09 09:2:54'),
	(49, 9, '2011-12-07 07:25:00' ),
	(50, 10, '2013-10-20 23:23:50');

-- Fill ExcursionPerson --
INSERT INTO ExcursionPerson (excursion_id, person_id) VALUES
	(41, 11), (42, 11), (42, 12), (43, 13), (44, 13), (45, 13),
	(46, 14), (46, 15), (46, 16), (47, 17), (47, 18), 
	(48, 18), (48, 19), (48, 20), (49, 18), (50, 20); 

-- Fill Stolen --
INSERT INTO Stolen (person_id, alien_id, ship_id, time) VALUES
	(14, 5, 21, '2005-10-19 10:23:54'), 
	(14, 5, 22, '2009-11-11 10:23:54'), 
	(12, 5, 23, '2010-10-19 10:23:54'), 
	(14, 5, 22, '2003-10-19 10:23:54'), 
	(15, 7, 24, '2004-10-19 10:23:54'); 

-- Fill kills --
INSERT INTO kills (person_id, alien_id, time) VALUES
	(14, 5, '2005-10-19 10:23:54'), 
	(14, 7, '2013-10-19 10:23:54'), 
	(15, 8, '2004-10-19 10:23:54'); 


-- 1 query task
WITH constants (F_start, T_end, N_amount, A_alien_id) AS (
	VALUES ('2004-10-19', '2014-10-19', 1, 5)
)
SELECT person_id FROM Stolen, constants
WHERE alien_id = A_alien_id
AND time >= TO_DATE(F_start, 'YYYY-MM-DD')
AND time <= TO_DATE(T_end, 'YYYY-MM-DD')
GROUP BY person_id, N_amount
HAVING COUNT(person_id) >= N_amount;

-- 2 query task
WITH constants (F_start, T_end, N_amount, H_person_id) AS (
	VALUES ('2004-10-19', '2014-10-19', 1, 14)
)
SELECT alien_id FROM Stolen, constants
WHERE person_id = H_person_id
AND time >= TO_DATE(F_start, 'YYYY-MM-DD')
AND time <= TO_DATE(T_end, 'YYYY-MM-DD')
GROUP BY alien_id, N_amount
HAVING COUNT(alien_id) >= N_amount;

-- 3 query task
WITH constants(f_start_date, t_end_date, n_steal_count, h_person_id) AS (
	VALUES('2004-10-19', '2014-10-19', 2, 14)
)
SELECT alien_id FROM stolen, constants
WHERE person_id = h_person_id 
AND time >= TO_DATE(f_start_date, 'YYYY-MM-DD') 
AND time <= TO_DATE(t_end_date, 'YYYY-MM-DD')
GROUP BY alien_id, n_steal_count
HAVING COUNT(alien_id) >= n_steal_count;

-- 4 query task
WITH constants (F_start, T_end, H_person_id) AS (
	VALUES ('2004-10-19', '2014-10-19', 14)
)
SELECT alien_id FROM kills, constants
WHERE person_id = H_person_id
AND time >= TO_DATE(F_start, 'YYYY-MM-DD')
AND time <= TO_DATE(T_end, 'YYYY-MM-DD')
GROUP BY alien_id;

-- 5 query task
WITH constants(h_person_id) AS (
	VALUES (14)
)
SELECT DISTINCT kills.alien_id 
FROM kills, stolen, constants
WHERE kills.person_id = h_person_id 
AND stolen.person_id = h_person_id 
AND kills.alien_id = stolen.alien_id;

-- 6 query task
WITH constants(f_start_date, t_end_date, n_steal_count) AS (
	VALUES ('2004-10-19', '2014-10-19', 1)
)
SELECT alien_id FROM stolen, constants
GROUP BY alien_id, n_steal_count
HAVING COUNT(person_id) 
	FILTER (WHERE time >= TO_DATE(f_start_date, 'YYYY-MM-DD') 
			AND time <= TO_DATE(t_end_date, 'YYYY-MM-DD'))
	>= n_steal_count;
