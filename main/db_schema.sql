CREATE DATABASE IF NOT EXISTS `edgar`;
SET CHARACTER SET utf8mb4;
USE `edgar`;

CREATE TABLE IF NOT EXISTS `sub` (
  `adsh` char(20) NOT NULL, -- fixed length so char rather than varchar
  `cik` int(10) NOT NULL,
  `name` varchar(150) NOT NULL,
  `sic` int(4) DEFAULT NULL,
  `countryba` varchar(2) NOT NULL,
  `stprba` varchar(2) DEFAULT NULL,
  `cityba` varchar(30) NOT NULL,
  `zipba` varchar(10) DEFAULT NULL,
  `bas1` varchar(40) DEFAULT NULL,
  `bas2` varchar(40) DEFAULT NULL,
  `baph` varchar(20) DEFAULT NULL,
  `countryma` varchar(2) DEFAULT NULL,
  `stprma` varchar(2) DEFAULT NULL,
  `cityma` varchar(30) DEFAULT NULL,
  `zipma` varchar(10) DEFAULT NULL,
  `mas1` varchar(40) DEFAULT NULL,
  `mas2` varchar(40) DEFAULT NULL,
  `countryinc` varchar(3) NOT NULL,
  `stprinc` varchar(2) DEFAULT NULL,
  `ein` int(10) DEFAULT NULL,
  `former` varchar(150) DEFAULT NULL,
  `changed` varchar(8) DEFAULT NULL,
  `afs` varchar(5) DEFAULT NULL,
  `wksi` tinyint(1) NOT NULL,
  `fye` char(4) NOT NULL, -- fixed length so char rather than varchar
  `form` varchar(10) NOT NULL,
  `period` date NOT NULL,
  `fy` int(4) NOT NULL,
  `fp` char(2) NOT NULL,
  `filed` date NOT NULL,
  `accepted` timestamp NOT NULL,
  `prevrpt` tinyint(1) NOT NULL,
  `detail` tinyint(1) NOT NULL,
  `instance` varchar(32) NOT NULL,
  `nciks` int(4) NOT NULL,
  `aciks` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`adsh`),
  KEY `name_idx` (`name`) -- not part of the schema just speeds up common queries, remove if import time more important
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `tag` (
  `tag` varchar(256) NOT NULL,
  `version` varchar(20) NOT NULL,
  `custom` tinyint(1) NOT NULL,
  `abstract` tinyint(1) NOT NULL,
  `datatype` varchar(20) DEFAULT NULL,
  `iord` varchar(1) NOT NULL,
  `crdr` varchar(1) DEFAULT NULL,
  `tlabel` varchar(512) DEFAULT NULL,
  `doc` text DEFAULT NULL,
  PRIMARY KEY (`tag`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `num` (
  `adsh` varchar(20) NOT NULL,
  `tag` varchar(256) NOT NULL,
  `version` varchar(20) NOT NULL,
  `coreg` varchar(256) DEFAULT NULL, -- column number in readme.htm is different to column number in data; important for import
  `ddate` date NOT NULL,
  `qtrs` int(8) NOT NULL,
  `uom` varchar(20) NOT NULL,
  `value` decimal(28,4) DEFAULT NULL,
  `footnote` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`adsh`,`tag`,`version`,`ddate`,`qtrs`,`uom`,`coreg`),
  FOREIGN KEY (adsh) REFERENCES sub(adsh),
  FOREIGN KEY (tag, version) REFERENCES tag(tag, version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `pre` (
  `adsh` varchar(20) NOT NULL,
  `report` int(6) NOT NULL,
  `line` int(6) NOT NULL,
  `stmt` varchar(2) NOT NULL,
  `inpth` tinyint(1) NOT NULL,
  `rfile` varchar(1) NOT NULL,
  `tag` varchar(256) NOT NULL,
  `version` varchar(20) NOT NULL,
  `plabel` varchar(512) NOT NULL,
  `negating` tinyint(1) NOT NULL, -- present in data but not documented in readme.htm
  PRIMARY KEY (`adsh`,`report`,`line`),
  FOREIGN KEY (adsh) REFERENCES sub(adsh),
  FOREIGN KEY (tag, version) REFERENCES tag(tag, version),
  FOREIGN KEY (adsh, tag, version) REFERENCES num(adsh, tag, version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;