CREATE TABLE IF NOT EXISTS `character_quests` (
  `charId` INT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(40) NOT NULL DEFAULT '',
  `var`  VARCHAR(20) NOT NULL DEFAULT '',
  `value` VARCHAR(255) ,
  `class_index` int(1) NOT NULL default '0',
  PRIMARY KEY (`charId`,`name`,`var`,`class_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;