#### Test Questions and answers
Q1. If initial car position out of field, should not execute any commands.

A1. 
```db2
   SELECT bks.title, bks.author, COUNT(b_bks.book_id) AS borrow_count FROM borrowed_books b_bks
JOIN
    books bks ON b_bks.book_id = bks.book_id
GROUP BY b_bks.book_id ORDER BY borrow_count DESC LIMIT 10;
```
Q2.Create a stored procedure that calculates the average number of days a book is borrowed before being returned. The procedure should take a book_id as input and return the average number of days.

A2.
```db2
CREATE DEFINER=`root`@`localhost` PROCEDURE `CalAvgeBorrowDuration`(IN bookId INT, OUT avgDuration DECIMAL(10,2))
BEGIN
    SELECT AVG(DATEDIFF(return_date, borrow_date)) INTO avgDuration
    FROM borrowed_books
    WHERE book_id = bookId AND return_date IS NOT NULL;
END
```
![demo](images/sql_q2_answer.png)
