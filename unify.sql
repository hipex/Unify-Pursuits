-- phpMyAdmin SQL Dump
-- version 3.5.8.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 10, 2013 at 01:23 PM
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE IF NOT EXISTS `services` (
  `serviceID` int(11) NOT NULL AUTO_INCREMENT,
  `serviceTitle` varchar(100) DEFAULT NULL,
  `serviceModule` varchar(100) DEFAULT NULL,
  `parentServiceID` int(11) NOT NULL,
  PRIMARY KEY (`serviceID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`serviceID`, `serviceTitle`, `serviceModule`, `parentServiceID`) VALUES
(0, 'group', 'group', 0),
(1, 'gmail', 'gmail', 0),
(2, 'gcal appointment', 'gcal_appointment', 3),
(3, 'gcal calendar', 'gcal_calendar', 0),
(4, 'evernote notebook', 'evernote_notebook', 0),
(5, 'evernote note', 'evernote_note', 4);

-- --------------------------------------------------------

--
-- Table structure for table `widgets`
--

CREATE TABLE IF NOT EXISTS `widgets` (
  `widgetID` int(11) NOT NULL AUTO_INCREMENT,
  `widgettypeID` int(11) NOT NULL,
  `parentID` int(11) NOT NULL,
  `preferences` varchar(100) NOT NULL,
  PRIMARY KEY (`widgetID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `WidgetToItem`
--

CREATE TABLE IF NOT EXISTS `WidgetToItem` (
  `WTIID` int(11) NOT NULL AUTO_INCREMENT,
  `widgetID` int(11) NOT NULL,
  `itemID` int(11) NOT NULL,
  PRIMARY KEY (`WTIID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `widgettypes`
--

CREATE TABLE IF NOT EXISTS `widgettypes` (
  `widgettypeID` int(11) NOT NULL AUTO_INCREMENT,
  `widgettypeModule` varchar(100) NOT NULL,
  `widgettypeTitle` varchar(100) NOT NULL,
  PRIMARY KEY (`widgettypeID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `widgettypes`
--

INSERT INTO `widgettypes` (`widgettypeID`, `widgettypeModule`, `widgettypeTitle`) VALUES
(1, 'widgettype_agenda', 'agenda'),
(2, 'widgettype_notebook', 'notebook');

-- --------------------------------------------------------

--
-- Table structure for table `WidgettypeToService`
--

CREATE TABLE IF NOT EXISTS `WidgettypeToService` (
  `WTSID` int(11) NOT NULL AUTO_INCREMENT,
  `widgettypeID` int(11) NOT NULL,
  `serviceID` int(11) NOT NULL,
  PRIMARY KEY (`WTSID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `WidgettypeToService`
--

INSERT INTO `WidgettypeToService` (`WTSID`, `widgettypeID`, `serviceID`) VALUES
(1, 1, 3),
(2, 2, 4),
(3, 1, 2);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
