--******* USERS *******
--create table users
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        email TEXT,
        name TEXT,
        password_hash TEXT,
        avatar TEXT,
        role TEXT
        );
--Create user:
--******* PROJECTS *******
--create table projects
    CREATE TABLE projects (
        project_id SERIAL PRIMARY KEY,
        title TEXT,
        image TEXT,
        description TEXT,
        category TEXT
        
        );
--update table
ALTER TABLE projects
ADD user_id INTEGER;

--Inser project
INSERT INTO projects(project_id, title, image, description, category) 
    VALUES (1, 'Food Truck App Design', 'image_url', 'This was my first project as a UX student', 'Design');

--******* COMMENTS *******
--create table comments
    CREATE TABLE comments (
        comment_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        project_id INTEGER
        content TEXT
        );