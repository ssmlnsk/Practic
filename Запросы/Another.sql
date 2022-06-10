CREATE TABLE Requests
(
  id_request INT NOT NULL,
  number_request VARCHAR(255) NOT NULL,
  date_create DATE NOT NULL,
  time_request VARCHAR(255) NOT NULL,
  number_client VARCHAR(255) NOT NULL,
  services VARCHAR(255) NOT NULL,
  status_request VARCHAR(255) NOT NULL,
  date_close DATE NOT NULL,
  rental_time VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_request)
);

CREATE TABLE Employeers
(
  id_employeer INT NOT NULL,
  post VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  login VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  lastLogIn VARCHAR(255) NOT NULL,
  StatusLogIn VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_employeer)
);

CREATE TABLE EntryHistory
(
  data_entry DATE NOT NULL,
  data_exit DATE NOT NULL,
  block VARCHAR(255) NOT NULL,
  id_employeer INT NOT NULL,
  FOREIGN KEY (id_employeer) REFERENCES Employeers(id_employeer)
);

CREATE TABLE Services
(
  id_service INT NOT NULL,
  name_service VARCHAR(255) NOT NULL,
  code_service VARCHAR(255) NOT NULL,
  price_for_hour VARCHAR(255) NOT NULL,
  id_request INT NOT NULL,
  PRIMARY KEY (id_service),
  FOREIGN KEY (id_request) REFERENCES Requests(id_request)
);

CREATE TABLE Clients
(
  number_client INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  passport VARCHAR(255) NOT NULL,
  datebirth DATE NOT NULL,
  address VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  id_request INT NOT NULL,
  PRIMARY KEY (number_client),
  FOREIGN KEY (id_request) REFERENCES Requests(id_request)
);