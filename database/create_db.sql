CREATE TABLE IF NOT EXISTS Users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    log_count INT DEFAULT 0,
    deleted TINYINT DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Activities (
    activity_id TEXT PRIMARY KEY,
    user_id TEXT,
    added at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Config (
    text_channel_id TEXT
)

-- CREATE TABLE IF NOT EXISTS movies_posters ()