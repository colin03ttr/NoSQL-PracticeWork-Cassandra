# NoSQL Course - Cassandra Practice Work 



COPY authors_publis(art_id,author,type,year,title,pages_start,pages_end,booktitle,
journal_series,journal_editor,journal_volume,journal_isbn,url,pos)
FROM './authors_publis_cleaned.csv' WITH HEADER = true AND DELIMITER=';';

```sql
USE DBLP;
```
```sql
SELECT * FROM publications;
```
![alt text](./images/image.png) 19693 rows output.
```sql
SELECT title FROM publications;
```
![alt text](./images/image-1.png) 19693 rows output.
```sql
SELECT booktitle FROM publications WHERE art_id='series/sci/2008-156';
```
![alt text](./images/image-2.png) 1 row output.

```sql
SELECT COUNT(*) FROM publications WHERE type = 'Book';
```
![alt text](./images/image-3.png) 1 row output.

```sql
SELECT COUNT(*) FROM publications WHERE booktitle = 'HICSS' ALLOW FILTERING;
```
![alt text](./images/image-4.png) 1 row input.

```sql
CREATE INDEX IF NOT EXISTS idx_booktitle ON publications(booktitle);
SELECT COUNT(*) FROM publications WHERE booktitle = 'HICSS';
```
![alt text](./images/image-5.png) Without the need of `ALLOW FILTERING`.

```sql
SELECT COUNT(*) FROM publications WHERE type = 'Article' AND booktitle = 'HICSS' ALLOW FILTERING;
```
![alt text](./images/image-6.png)

```sql
SELECT COUNT(*) FROM authors WHERE pos = 3;
```
![alt text](./images/image-7.png)

```sql
SELECT COUNT(*) FROM authors WHERE pos > 3 ALLOW FILTERING;
```
![alt text](./images/image-8.png)

```sql
SELECT COUNT(*) FROM publications WHERE token(art_id) < 0;
```
![alt text](./images/image-9.png) 
```sql
SELECT art_id, token(art_id) FROM publications;
```
![alt text](./images/image-10.png) 19 693 rows output.