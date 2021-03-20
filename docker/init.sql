CREATE TABLE scans
( 
    scan_id uuid PRIMARY KEY,
    status varchar(20) NOT NULL,
    date timestamp NOT NULL
);

CREATE TABLE scan_properties
( 
    scan_id uuid PRIMARY KEY,
    timeout int NOT NULL,
    CONSTRAINT fk_scan_id
      FOREIGN KEY(scan_id) 
	  REFERENCES scans(scan_id)
);