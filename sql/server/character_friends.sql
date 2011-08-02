CREATE TABLE IF NOT EXISTS `character_friends` (
  `charId` INT UNSIGNED NOT NULL default 0,
  `friendId` INT UNSIGNED NOT NULL DEFAULT 0,
  `relation` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`charId`,`friendId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;