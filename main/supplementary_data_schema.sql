USE `edgar`;

CREATE TABLE IF NOT EXISTS `ciktotick` (
  `ticker` varchar(8) NOT NULL,
  `cik` int(11) NOT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`ticker`,`cik`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `industry` (
  `sic` int(11) DEFAULT NULL,
  `cat` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;