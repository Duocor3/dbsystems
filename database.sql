CREATE TABLE city (
  id VARCHAR(50),
  lat DECIMAL(9,6),
  long DECIMAL(9,6)
);

INSERT INTO city (id, lat, long)
VALUES 
  ('New York City', 40.7128, -74.0060),
  ('Los Angeles', 34.0522, -118.2437),
  ('Chicago', 41.8781, -87.6298),
  ('Houston', 29.7604, -95.3698),
  ('Phoenix', 33.4484, -112.0740);

CREATE TABLE temp (
  tmp DECIMAL(5,2),
  cityid VARCHAR(50)
);

INSERT INTO temp (tmp, cityid)
VALUES 
  (78.50, 'New York City'),
  (82.25, 'Los Angeles'),
  (74.20, 'Chicago'),
  (91.60, 'Houston'),
  (102.30, 'Phoenix');

CREATE TABLE reports (
  user VARCHAR(50),
  tmp DECIMAL(5,2),
  cityid VARCHAR(50)
);

INSERT INTO reports (user, tmp, cityid)
VALUES 
  ('John', 78.50, 'New York City'),
  ('Sarah', 82.25, 'Los Angeles'),
  ('Michael', 74.20, 'Chicago'),
  ('Emma', 91.60, 'Houston'),
  ('James', 102.30, 'Phoenix');