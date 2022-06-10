CREATE TABLE IF NOT EXISTS EntryHistory (
id INT PRIMARY KEY,
data_entry DATE NOT NULL,
data_exit DATE,
block BOOL,
id_employeer VARCHAR(255) NOT NULL,
FOREIGN KEY (id_employeer) REFERENCES Employeers (id_employeer)
);