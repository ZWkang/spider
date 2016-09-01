-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2016-09-01 23:20:59
-- 服务器版本： 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `lagou`
--

-- --------------------------------------------------------

--
-- 表的结构 `position`
--

CREATE TABLE IF NOT EXISTS `position` (
  `lagou_positionId` int(18) NOT NULL COMMENT '//职位id',
  `lagou_positionName` varchar(50) NOT NULL COMMENT '//职位名称',
  `lagou_education` varchar(20) NOT NULL COMMENT '//职位学历要求',
  `lagou_jobNature` varchar(20) NOT NULL COMMENT '//工作性质(全职之类)',
  `lagou_workYear` varchar(20) NOT NULL COMMENT '//工作经验',
  `lagou_createTime` varchar(40) NOT NULL COMMENT '//职位创建时间',
  `lagou_companyShortName` varchar(20) NOT NULL COMMENT '//公司短名',
  `lagou_companyId` int(20) NOT NULL COMMENT '//公司id',
  `lagou_salary` varchar(20) NOT NULL COMMENT '//工资范围',
  `lagou_city` varchar(18) NOT NULL COMMENT '//职位地址',
  `lagou_positionAdvantage` varchar(50) NOT NULL COMMENT '//职位诱惑',
  `lagou_companyLogo` varchar(100) NOT NULL COMMENT '//公司logo',
  `lagou_industryField` varchar(20) NOT NULL COMMENT '//公司领域',
  `lagou_companyLabelList` varchar(100) NOT NULL COMMENT '//公司标签',
  `lagou_financeStage` varchar(30) NOT NULL COMMENT '//公司投资阶段',
  `lagou_district` varchar(30) NOT NULL COMMENT '//公司区域',
  `lagou_companySize` varchar(30) NOT NULL COMMENT '//公司大小规模',
  `lagou_companyFullName` varchar(100) NOT NULL COMMENT '//公司全名',
  `lagou_lastLogin` int(20) NOT NULL COMMENT '//最后登录时间',
  `lagou_businessZones` varchar(50) DEFAULT NULL COMMENT '//公司地址',
  `lagou_formatCreateTime` varchar(50) NOT NULL COMMENT '//发布时间在什么时候之前',
  `lagou_imState` varchar(20) NOT NULL COMMENT '//是否在状态',
  `lagou_score` int(10) DEFAULT '0' COMMENT '//分数',
  `lagou_adWord` int(10) NOT NULL DEFAULT '0' COMMENT '//关键词',
  `lagou_explain` varchar(50) DEFAULT NULL COMMENT '//解释',
  `lagou_plus` varchar(50) DEFAULT NULL COMMENT '//加',
  `lagou_pcShow` int(10) NOT NULL DEFAULT '0' COMMENT '//桌面',
  `lagou_appShow` int(10) NOT NULL DEFAULT '0' COMMENT '//应用程序显示',
  `lagou_deliver` int(10) NOT NULL DEFAULT '0' COMMENT '//运送',
  `lagou_gradeDescription` varchar(100) DEFAULT NULL COMMENT '//等级描述',
  `lagou_approve` int(10) NOT NULL DEFAULT '1' COMMENT '//批准',
  `lagou_publisherId` int(18) NOT NULL COMMENT '//出版商id',
  PRIMARY KEY (`lagou_positionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
