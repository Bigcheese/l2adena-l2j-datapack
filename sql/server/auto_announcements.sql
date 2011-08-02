CREATE TABLE IF NOT EXISTS `auto_announcements` (
  `id` INT(11) NOT NULL,
  `initial` BIGINT(20) NOT NULL,
  `delay` BIGINT(20) NOT NULL,
  `cycle` INT(11) NOT NULL,
  `memo` TEXT DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;