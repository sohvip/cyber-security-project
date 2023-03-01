create table if not exists users (
    id serial primary key,
    username text unique,
    password text,
    type integer
);

create table if not exists categories (
    id serial primary key,
    category text
);

create table if not exists posts (
    id serial primary key,
    title text,
    content text,
    user_id integer references users on delete cascade,
    category_id integer references categories on delete cascade,
    sent_at timestamp
);

create table if not exists comments (
    id serial primary key,
    comment text,
    user_id integer references users on delete cascade,
    post_id integer references posts on delete cascade,
    sent_at timestamp
);

create table if not exists likes (
    id serial primary key,
    liked integer,
    user_id integer references users on delete cascade,
    post_id integer references posts on delete cascade
);