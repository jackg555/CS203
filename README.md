# CS203

To Create Database and Tables:
python db.py

(if possible add feature where ipricetype can be both kg and each as some itmes you can buy per kg and buy per item)

INSERT INTO Items (iid, iname, iquantity, ipricetype) VALUES (1, 'Mince', 'kg', 'kg'), (2, 'Chicken', 'kg', 'kg'), (3, 'Rice', '500g', 'ea');

INSERT INTO Supermarkets (sid, sname, slocation, snumber) VALUES (1, 'New World', 'Ilam', 033435646), (2, 'Packnsave', 'Riccarton', 033489727), (3, 'Countdown', 'Avonhead', 033584765);

INSERT INTO SupermarketsItems (iid, sid, price) VALUES (1, 1, 20), (1, 2, 19), (1, 3, 18), (2, 1, 15), (2, 2, 14), (2, 3, 13), (3, 1, 4), (3, 2, 3), (3, 3, 2);
