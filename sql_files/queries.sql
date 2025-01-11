-- GROUP 136
-- Michelle Cheng

-- --------------------------------------------------------



-- CUSTOMERS --------------------------------------------------------

-- Get all Customers and their first name and last name for Customers Page
SELECT customer_id, first_name, last_name FROM Customers

-- Get a single customer's data for the Update Customer form
SELECT customer_id, first_name, last_name, email, birthdate FROM Customers
WHERE customer_id = :customer_ID_selected_from_browse_customer_page

-- Update a row for a Customer
UPDATE Customers
SET first_name = :first_nameInput, last_name = :last_nameInput, email = :emailInput, birthdate = :birthdateInput
WHERE :customer_ID_selected_from_browse_customer_page

-- Insert a new customer
INSERT INTO `Customers` (`first_name`, `last_name`, `email`, `birthdate`) 
VALUES (:first_nameInput, :last_nameInput, :emailInput, :birthdateInput)

-- Delete a customer
DELETE FROM Customers
WHERE customer_id = :customer_ID_selected_from_browse_customer_page


-- Search a customer by last name
SELECT * FROM Customers
WHERE last_name = :customer_last_name_input



-- ITEMS --------------------------------------------------------

-- Get all Items and their names and prices for the Items page
SELECT item_id, item_name, item_price FROM Items

-- Get a single item's data for the Update Item form
SELECT item_id, item_name, item_price FROM Items
WHERE item_id = :item_ID_selected_from_browse_item_page

-- Update a row for an Item
UPDATE Items
SET item_name = :item_nameInput, item_price = :item_priceInput
WHERE :item_ID_selected_from_browse_item_page;

-- Insert a new item
INSERT INTO `Items` (`item_name`, `item_price`) 
VALUES (:item_nameInput, :item_priceInput)

-- Delete an Item
DELETE FROM Items
WHERE item_id = :item_ID_selected_from_browse_item_page



-- LOCATIONS --------------------------------------------------------

-- Get all location cities for the Locations page
SELECT location_name FROM Locations

-- Get a single Location's data for the Update Location form
SELECT location_id, location_name FROM Locations
WHERE location_id = :location_ID_selected_from_browse_location_page

-- Update a row for a Location
UPDATE Items
SET location_name = :location_nameInput
WHERE :locawtion_ID_selected_from_browse_location_page;

-- Insert a new location
INSERT INTO `Locations` (`location_name`) 
VALUES (:location_nameInput)

-- Delete a location
DELETE FROM Items
WHERE location_id = :location_ID_selected_from_browse_location_page


-- ORDERS--------------------------------------------------------

-- Get all orders and their dates, locations, customers, and totals for the orders page

SELECT order_id, order_date, Locations.location_name, CONCAT(Customers.first_name, ' ', Customers.last_name), order_total FROM Orders
INNER JOIN Customers ON Orders.customer_id = Customers.customer_id
INNER JOIN Locations ON Orders.location_id = Locations.location_id
ORDER BY order_id

-- Populate Customers dropdown
SELECT CONCAT(Customers.first_name, ' ', Customers.last_name), customer_id FROM Customers

-- Populate Locations dropdown
SELECT location_name, location_id FROM Locations

-- Subquery to get Customer's Full Name
SELECT CONCAT(Customers.first_name, ' ', Customers.last_name) FROM Customers

-- Get a single Order's data for the Update Order form
SELECT order_id, order_date, location_id, customer_id, order_total FROM Orders
WHERE order_id = :order_ID_selected_from_browse_order_page

-- Update a row for an Order
UPDATE Orders
SET order_date = :order_dateInput, location_id = :location_idFromDropdown, customer_id = :customer_idFromDropdown
WHERE :order_ID_selected_from_browse_order_page


-- Insert a new Order
INSERT INTO `Orders`(`order_date`, `location_id`, `customer_id`)
VALUES (:order_dateInput, :location_idFromDropdown, :customer_idFromDropdown)

-- Delete an Order
DELETE FROM Orders
WHERE order_id = :order_ID_selected_from_browse_order_page

-- Update order_total column (To be used in procedure)
UPDATE Orders
SET order_total = ( 
   SELECT SUM(Order_Details.item_total)
   FROM Order_Details
   WHERE order_id = :order_ID_selected_from_browse_order_page
)
WHERE order_id = :order_ID_selected_from_browse_order_page


-- ORDER_DETAILS --------------------------------------------------------

-- Get all order details and their order details IDs, order IDs, item IDs, item quantities, and items totals for the Order Details page
SELECT order_detail_id, Orders.order_id, Items.item_name, item_quantity, item_total
FROM Order_Details
INNER JOIN Orders ON Order_Details.order_id = Orders.order_id
INNER JOIN Items ON Order_Details.item_id = Items.item_id
ORDER BY order_detail_id

-- Populate Order ID Dropdown
SELECT order_id FROM Orders

-- Populate Items Dropdown
SELECT item_id, item_name FROM Items

-- Get a single Order's data for the Update Order form
SELECT order_detail_id, order_id, item_id, item_quantity, item_total FROM Order_Details
WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page

-- Update a row for an Order Details
UPDATE Order_Details
SET order_id= :order_idFromDropdown, item_id = :item_idFromDropdown, item_quantity = :item_quantityInput
WHERE :order_detail_id_selected_from_browse_order_page

-- Insert a new Order
INSERT INTO `Order_Details`(`order_id`, `item_id`, `item_quantity`)
VALUES (:order_idFromDropdown, :item_idFromDropdown :item_quantityInput)

-- Delete an Order
DELETE FROM Order_Details
WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page

-- Update unit_cost column
UPDATE Order_Details
	SET unit_cost = (
	SELECT item_price 
	FROM Items
	INNER JOIN Order_Details ON Items.item_id = Order_Details.item_id
	WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page)
    WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page

-- Update item_total column
UPDATE Order_Details
SET item_total = (
    SELECT unit_cost * item_quantity as item_total
    FROM Order_Details
    WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page
)
WHERE order_detail_id = :order_detail_id_selected_from_browse_order_details_page