CREATE TABLE users (
  id            SERIAL PRIMARY KEY,
  username      TEXT NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE transactions (
  id                 SERIAL PRIMARY KEY,
  user_id            INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind TEXT          NOT NULL CHECK(kind IN ('expense', 'income')),
  transaction_date   DATE NOT NULL DEFAULT CURRENT_DATE,
  amount             NUMERIC NOT NULL,
  description        TEXT NOT NULL
);
