-- Create tables
drop table if exists users;
create table users (
    id serial primary key,
    name varchar(255),
    email varchar(255)
);

-- Insert sample data
insert into users (name, email) values
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');
