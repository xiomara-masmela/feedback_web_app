--create Databse
createdb feedback_app

--connect with database
psql feedback_app

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
        category TEXT,
        project_link TEXT,
        user_id INTEGER, 
        CONSTRAINT FK_projects_users FOREIGN KEY (user_id)
            REFERENCES users(user_id)
        
        );
--update table
ALTER TABLE projects ADD user_id INTEGER;


--Insert project
INSERT INTO projects( title, image, description, category, user_id) 
    VALUES ('Lorem ipsum', 'https://res.cloudinary.com/dtdhdix1f/image/upload/v1631784379/feedback-app/sbl1fgqoc1n1a0mkkvo8.jpg','Design', 9);

--Update Project
UPDATE projects SET title="This is edited" WHERE project_id = 5;

--******* COMMENTS *******
--create table comments
        CREATE TABLE comments (
        comment_id SERIAL PRIMARY KEY,
        content TEXT,
        project_id INTEGER,
        user_id INTEGER, 
        CONSTRAINT FK_comments_users FOREIGN KEY (user_id)
            REFERENCES users(user_id)
        
        );