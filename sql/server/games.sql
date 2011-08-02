CREATE TABLE IF NOT EXISTS `games` (
  `id` INT NOT NULL default 0,
  `idnr` INT NOT NULL default 0,
  `number1` INT NOT NULL default 0,
  `number2` INT NOT NULL default 0,
  `prize` INT NOT NULL default 0,
  `newprize` INT NOT NULL default 0,
  `prize1` INT NOT NULL default 0,
  `prize2` INT NOT NULL default 0,
  `prize3` INT NOT NULL default 0,
  `enddate` bigint(13) unsigned NOT NULL DEFAULT '0',
  `finished` INT NOT NULL default 0,
  PRIMARY KEY (`id`,`idnr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;