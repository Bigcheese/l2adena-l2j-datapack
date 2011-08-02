CREATE TABLE IF NOT EXISTS `character_shortcuts` (
  `charId` INT UNSIGNED NOT NULL default 0,
  `slot` decimal(3) NOT NULL default 0,
  `page` decimal(3) NOT NULL default 0,
  `type` decimal(3) ,
  `shortcut_id` decimal(16) ,
  `level` varchar(4) ,
  `class_index` int(1) NOT NULL default '0',
  PRIMARY KEY (`charId`,`slot`,`page`,`class_index`),
  KEY `shortcut_id` (`shortcut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;