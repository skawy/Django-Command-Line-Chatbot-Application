CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone INT,
    name VARCHAR(30),
    email VARCHAR(60),
    physical_address VARCHAR(60)
);

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(1000),
    response VARCHAR(1000),
    log_time DATE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(1000),
    user_id INT,
    start_message_id INT,
    end_message_id INT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (start_message_id) REFERENCES logs (id),
    FOREIGN KEY (end_message_id) REFERENCES logs (id)

);
