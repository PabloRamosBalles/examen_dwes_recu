-- create database examem_dwes_recu;
use examem_dwes_recu;

-- create table user(
--     id int unsigned auto_increment primary key,
--     email varchar(150) unique,
--     username varchar(150),
--     password varchar(255)
-- )
create table productos(
    id int unsigned auto_increment primary key,
    nombre varchar(100)
);

-- insert into user('email','password','username') values ('b', 'b', 'c');