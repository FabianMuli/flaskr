drop table if exists comments;
create table comments(
    id integer primary key autoincrement,
    'title' text not null,
    'text' varchar(100) not null
);

drop table if exists users;
create table users(
    id integer primary key autoincrement,
    'name' text not null,
    'email' text not null,
    'password' text not null,
    'phone' numeric not null
);

drop table if exists messages;
create table messages(
    id integer primary key autoincrement,
    'user' text not null,
    'message' varchar(100) not null
);