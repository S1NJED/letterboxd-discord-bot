CREATE TABLE IF NOT EXISTS Users (
    username TEXT PRIMARY KEY,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Activities (
    activity_id TEXT PRIMARY KEY,
    username TEXT,
    added at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (username) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Config (
    text_channel_id TEXT
)

-- CREATE TABLE IF NOT EXISTS movies_posters ()