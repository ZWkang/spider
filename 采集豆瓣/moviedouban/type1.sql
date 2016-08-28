-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2016-08-28 16:56:27
-- 服务器版本： 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `moviedouban`
--

-- --------------------------------------------------------

--
-- 表的结构 `type1`
--

CREATE TABLE IF NOT EXISTS `type1` (
  `movie_id` int(18) NOT NULL COMMENT '//电影id',
  `movie_name` varchar(100) NOT NULL COMMENT '//电影名字',
  `movie_url` varchar(100) NOT NULL COMMENT '//电影链接',
  `movie_type` varchar(64) NOT NULL COMMENT '//电影类型分类',
  `movie_regions` varchar(20) NOT NULL COMMENT '//电影上映地区',
  `movie_release_date` varchar(40) NOT NULL COMMENT '//电影上映时间',
  `type_rank` int(5) NOT NULL COMMENT '//当前分类权重',
  `movie_image` varchar(100) NOT NULL COMMENT '//电影图片',
  `movie_actor` varchar(60) NOT NULL COMMENT '//电影演员',
  `movie_score` float NOT NULL COMMENT '//电影得分',
  `vote_count` int(10) NOT NULL COMMENT '//电影投票人数',
  `rating_two` int(10) NOT NULL COMMENT '//不知名的也写进来',
  PRIMARY KEY (`movie_id`),
  UNIQUE KEY `movie_id` (`movie_id`),
  KEY `type_rank` (`type_rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
