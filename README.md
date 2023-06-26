# CS203
----EXECUTE LINE BY LINE----

To Create Database and Tables:
python db.py

(if possible add feature where ipricetype can be both kg and each as some itmes you can buy per kg and buy per item)

INSERT INTO Items (iid, iname, iquantity, ipricetype) VALUES (1, 'Mince', 'kg', 'kg'), (2, 'Chicken', 'kg', 'kg'), (3, 'Rice', '500g', 'ea'), (4, 'Apples', 'each', 'ea'), (5, 'Tomatoes', 'kg', 'kg'), (6, 'Bread', 'loaf', 'ea'), (7, 'Salmon', '100g', 'ea'), (8, 'Oranges', 'kg', 'kg'), (9, 'Eggs', 'dozen', 'ea'), (10, 'Pasta', '500g', 'ea');

INSERT INTO Supermarkets (sid, sname, slocation, snumber) VALUES (1, 'New World', 'Ilam', 033435646), (2, 'Packnsave', 'Riccarton', 033489727), (3, 'Countdown', 'Avonhead', 033584765);

INSERT INTO SupermarketsItems (iid, sid, price) VALUES (1, 1, 20), (1, 2, 19), (1, 3, 18), (2, 1, 15), (2, 2, 14), (2, 3, 13), (3, 1, 4), (3, 2, 3), (3, 3, 2), (4, 1, 2), (4, 2, 2.5), (4, 3, 2.2), (5, 1, 3), (5, 2, 3.5), (5, 3, 3.2), (6, 1, 2.5), (6, 2, 2.3), (6, 3, 2.8), (7, 1, 10), (7, 2, 11), (7, 3, 9.5), (8, 1, 2.5), (8, 2, 2.8), (8, 3, 2.3), (9, 1, 3), (9, 2, 3.2), (9, 3, 2.8), (10, 1, 1.5), (10, 2, 1.7), (10, 3, 1.3);
