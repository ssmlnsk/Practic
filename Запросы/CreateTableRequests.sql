CREATE TABLE IF NOT EXISTS Requests (
id_request INT PRIMARY KEY auto_increment,
number_request VARCHAR(255) NOT NULL,
date_create VARCHAR(255) NOT NULL,
time_request VARCHAR(255) NOT NULL,
number_client INT NOT NULL,
services VARCHAR(255) NOT NULL,
status_request VARCHAR(255) NOT NULL,
date_close VARCHAR(255) NOT NULL,
rental_time VARCHAR(255) NOT NULL,
FOREIGN KEY (number_client) REFERENCES Clients (number_client),
FOREIGN KEY (services) REFERENCES Services (id_service)
); 