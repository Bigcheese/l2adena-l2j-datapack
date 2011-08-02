CREATE TABLE IF NOT EXISTS `cursed_weapons` (
  `itemId` INT,
  `charId` INT UNSIGNED NOT NULL DEFAULT 0,
  `playerKarma` INT DEFAULT 0,
  `playerPkKills` INT DEFAULT 0,
  `nbKills` INT DEFAULT 0,
  `endTime` bigint(13) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`itemId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;