USE `edgar`;

CREATE TABLE IF NOT EXISTS `industry` (
  `sic` int(11) DEFAULT NULL,
  `cat` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`sic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `price` (
  `date` date NOT NULL,
  `cik` int(10) NOT NULL,
  `name` varchar(150) NOT NULL,
  `symbol` varchar(6) NOT NULL,
  `open` decimal(18, 4) DEFAULT NULL,
  `high` decimal(18, 4) DEFAULT NULL,
  `low` decimal(18, 4) DEFAULT NULL,
  `close` decimal(18, 4) DEFAULT NULL,
  `adj close` decimal(18, 4) DEFAULT NULL,
  `volume` int DEFAULT NULL,
  PRIMARY KEY (`date`, `symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;