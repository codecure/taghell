/*!40101 SET NAMES utf8 */;


# Дамп таблицы photo
# ------------------------------------------------------------
CREATE TABLE `photo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `src` text,
  `created_at` datetime DEFAULT NULL,
  `likes` int(11) DEFAULT NULL,
  `tags` text,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `tags` (`tags`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


# Дамп таблицы tag
# ------------------------------------------------------------

CREATE TABLE `tag` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT '',
  `off` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `off` (`off`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
