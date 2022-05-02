CREATE TABLE IF NOT EXISTS mainmenu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    handle text NOT NULL,
    psw text NOT NULL,
    friends text NOT NULL,
    to_friend text NOT NULL,
    from_friend text NOT NULL
)