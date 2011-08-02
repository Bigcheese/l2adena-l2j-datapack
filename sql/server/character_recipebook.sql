CREATE TABLE IF NOT EXISTS `character_recipebook` (
  `charId` INT UNSIGNED NOT NULL default 0,
  `id` decimal(11) NOT NULL default 0,
  `classIndex` TINYINT NOT NULL DEFAULT 0,
  `type` INT NOT NULL default 0,
  PRIMARY KEY (`id`,`charId`,`classIndex`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;