-- phpMyAdmin SQL Dump
-- version 3.5.8.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 30, 2013 at 04:51 PM
-- Server version: 5.5.31
-- PHP Version: 5.4.15

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `unify`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE IF NOT EXISTS `items` (
  `itemID` int(11) NOT NULL AUTO_INCREMENT,
  `serviceID` int(11) DEFAULT NULL,
  `parameter` varchar(100) DEFAULT NULL,
  `parentID` int(11) DEFAULT NULL,
  PRIMARY KEY (`itemID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`itemID`, `serviceID`, `parameter`, `parentID`) VALUES
(0, 0, 'hoofdgroep', 0);

-- --------------------------------------------------------

--
-- Table structure for table `labels`
--

CREATE TABLE IF NOT EXISTS `labels` (
  `labelID` int(11) NOT NULL AUTO_INCREMENT,
  `serviceID` int(11) NOT NULL,
  `parameter` varchar(100) NOT NULL,
  `lastupdate` datetime NOT NULL,
  PRIMARY KEY (`labelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE IF NOT EXISTS `services` (
  `serviceID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `module` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`serviceID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`serviceID`, `name`, `module`) VALUES
(0, 'group', 'group'),
(1, 'gmail', 'gmail'),
(2, 'calendar', 'gcal');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
