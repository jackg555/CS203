# CS203

To Create Database and Tables:
python db.py

NOT WORKING:
(if possible add feature where ipricetype can be both kg and each as some itmes you can buy per kg and buy per item)
Query for Inserting Food Items:

INSERT INTO Items (iid, iname, iquantity, ipricetype) 
VALUES (1, 'Mince', 'kg', 'kg'), (2, 'Chicken', 'kg', 'kg'), 
(3, 'Rice', '500g', 'ea'), (4, 'Tomato', 'kg', 'kg'), (5, 'Onion', 'kg', 'kg'), 
(6, 'Carrot', 'kg', 'kg'), (7, 'Bread', '700g', 'ea');

Query for Inserting Supermarkets:

INSERT INTO Supermarkets (sid, sname, slocation, snumber)

VALUES (1, 'New World', 'Ilam', 033435646), (2, 'Packnsave', 'Riccarton', 033489727), (3, 'Countdown', 'Avonhead', 033584765);

BASIC QUERY:
INSERT INTO Items (iid, iname, iquantity, ipricetype) VALUES (1, 'Mince', 'kg', 'kg');

INSERT INTO Supermarkets (sid, sname, slocation, snumber) VALUES (1, 'New World', 'Ilam', 033435646);

INSERT INTO Lists (lid, lname, ldate) VALUES (1, 'List 1', 2023-06-15);

INSERT INTO ListsItems (lid, iid, lquantity) VALUES (1, 2, 1);
