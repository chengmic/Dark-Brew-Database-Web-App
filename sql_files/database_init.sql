-- GROUP 136
-- Michelle Cheng


-- --------------------------------------------------------
-- phpMyAdmin SQL Dump
-- version 5.2.0-1.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 14, 2022 at 04:50 AM
-- Server version: 10.6.9-MariaDB-log
-- PHP Version: 7.4.30

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_chengmic`
--

-- --------------------------------------------------------


-- Drop Tables if Exist
DROP TABLE IF EXISTS `Order_Details`;
DROP TABLE IF EXISTS `Orders`;
DROP TABLE IF EXISTS `Locations`;
DROP TABLE IF EXISTS `Items`;
DROP TABLE IF EXISTS `Customers`;


-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--

CREATE TABLE `Customers` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `birthdate` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`customer_id`, `first_name`, `last_name`, `email`, `birthdate`) VALUES
(1, 'Cayde', 'Meowington', 'cayde@meow.com', '2020-05-27'),
(2, 'Tom', 'Nook', 'tomnook@bells.com', '2001-05-30'),
(3, 'Brewster', 'Pigeon', 'brewster@coo.com', '2001-10-15'),
(4, 'Filbert', 'Blue', 'filbert@food.com', '2001-06-05'),
(5, 'Benjamin', 'Sisko', 'bensisko@starfleet.com', '1993-01-03');

-- --------------------------------------------------------

--
-- Table structure for table `Items`
--

CREATE TABLE `Items` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(45) NOT NULL,
  `item_price` decimal(4,2) DEFAULT '0.00',
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Items`
--

INSERT INTO `Items` (`item_id`, `item_name`, `item_price`) VALUES
(1, 'Dark Roast', '1.00'),
(2, 'Cold Brew', '4.50'),
(3, 'Latte', '3.00'),
(4, 'Mocha', '3.00'),
(5, 'Crossiant', '2.00');

-- --------------------------------------------------------

--
-- Table structure for table `Locations`
--

CREATE TABLE `Locations` (
  `location_id` int(11) NOT NULL,
  `location_name` varchar(45) NOT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Locations`
--

INSERT INTO `Locations` (`location_id`, `location_name`) VALUES
(1, 'San Diego Convoy'),
(2, 'San Diego Balboa'),
(3, 'Riverside'),
(4, 'Long Beach'),
(5, 'Murrieta');

-- --------------------------------------------------------

--
-- Table structure for table `Orders`
--

CREATE TABLE `Orders` (
  `order_id` int(11) NOT NULL,
  `order_date` date NOT NULL,
  `location_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `order_total` decimal(6,2) DEFAULT'0.00',
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Orders`
--

INSERT INTO `Orders`(`order_id`, `order_date`, `location_id`, `customer_id`, `order_total`) VALUES
(1, '2022-01-01', 1, 1, 6.50),
(2, '2022-01-01', 1, 1, 3.00),
(3, '2022-01-01', 3, 2, 6.00),
(4, '2022-01-01', 4, 4, 0.00),
(5, '2022-01-01', 5, NULL, 3.00);

-- --------------------------------------------------------

--
-- Table structure for table `Order_Details`
--

CREATE TABLE `Order_Details` (
  `order_detail_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `item_id` int(11),
  `unit_cost` decimal(6,2) DEFAULT 0.00,
  `item_quantity` int(11) NOT NULL,
  `item_total` decimal(6,2) DEFAULT'0.00',
  PRIMARY KEY (`order_detail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Order_Details`
--

INSERT INTO `Order_Details` (`order_detail_id`, `order_id`, `item_id`, `unit_cost`, `item_quantity`, `item_total`) VALUES
(1, 1, 2, '4.50', 1, '4.50'),
(2, 1, 5, '2.00', 1, '2.00'),
(3, 2, 1, '1.00', 3, '3.00'),
(4, 3, 3, '3.00', 2, '6.00'),
(5, 5, 4, '3.00', 1, '3.00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Customers`
--
ALTER TABLE `Customers`
  ADD UNIQUE KEY `customer_id_UNIQUE` (`customer_id`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`);

--
-- Indexes for table `Items`
--
ALTER TABLE `Items`
  ADD UNIQUE KEY `item_id_UNIQUE` (`item_id`),
  ADD UNIQUE KEY `item_name_UNIQUE` (`item_name`);

--
-- Indexes for table `Locations`
--
ALTER TABLE `Locations`
  ADD UNIQUE KEY `location_id_UNIQUE` (`location_id`),
  ADD UNIQUE KEY `location_name_UNIQUE` (`location_name`);

--
-- Indexes for table `Orders`
--
ALTER TABLE `Orders`
  ADD UNIQUE KEY `order_id_UNIQUE` (`order_id`),
  ADD KEY `fk_Orders_Customers_idx` (`customer_id`),
  ADD KEY `fk_Orders_Locations1_idx` (`location_id`);

--
-- Indexes for table `Order_Details`
--
ALTER TABLE `Order_Details`
  ADD UNIQUE KEY `order_detail_id_UNIQUE` (`order_detail_id`),
  ADD KEY `fk_Order_Items_Orders1_idx` (`order_id`),
  ADD KEY `fk_Order_Items_Items1_idx` (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Customers`
--
ALTER TABLE `Customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Items`
--
ALTER TABLE `Items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Locations`
--
ALTER TABLE `Locations`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Orders`
--
ALTER TABLE `Orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Order_Details`
--
ALTER TABLE `Order_Details`
  MODIFY `order_detail_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Orders`
--
ALTER TABLE `Orders`
  ADD CONSTRAINT `fk_Orders_Customers` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Orders_Locations` FOREIGN KEY (`location_id`) REFERENCES `Locations` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Order_Details`
--
ALTER TABLE `Order_Details`
  ADD CONSTRAINT `fk_Order_Details_Items` FOREIGN KEY (`item_id`) REFERENCES `Items` (`item_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Order_Details_Orders` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`) ON DELETE CASCADE;


SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;