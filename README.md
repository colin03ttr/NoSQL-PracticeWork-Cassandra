# NoSQL Course - Cassandra Practice Work 

## Create Database on Cassandra

### Files transfer

```bash
docker cp .\DBLP.tar.gz cassandraServer:/
```
```
Successfully copied 4.84MB to cassandraServer:/
```

On Docker Desktop, I open the CLI and extract the compressed data :

```
# ls
bin  boot  __cacert_entrypoint.sh  DBLP.tar.gz  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
# tar xzvf DBLP.tar.gz
DBLP/
DBLP/._.DS_Store
DBLP/.DS_Store
DBLP/._authors_publis.csv
DBLP/authors_publis.csv
DBLP/._authors.csv
DBLP/authors.csv
DBLP/._liste.csv
DBLP/liste.csv
DBLP/._DBLP_publis.csv
DBLP/DBLP_publis.csv
DBLP/DBLP.json
# ls     
bin  boot  __cacert_entrypoint.sh  DBLP  DBLP.tar.gz  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```
Using the cqlsh command, I can start making queries to create a database and import the data.
```
# cqlsh
Connected to Test Cluster at 127.0.0.1:9042
[cqlsh 6.2.0 | Cassandra 5.0.2 | CQL spec 3.4.7 | Native protocol v5]
Use HELP for help.
cqlsh> CREATE KEYSPACE IF NOT EXISTS DBLP
   ... WITH REPLICATION =
   ... { 'class' : 'SimpleStrategy', 'replication_factor': 3 };

Warnings :
Your replication factor 3 for keyspace dblp is higher than the number of nodes 1

cqlsh> USE DBLP;
```
I created a database called `DBLP`, now lets create the table `publications`, and an index for the publication `type`:
```
cqlsh:dblp> CREATE TABLE publications (
        ... art_id TEXT, type TEXT, title text, pages_start INT, pages_end int, booktitle text,
        ... journal_series text, journal_editor text, journal_volume int, journal_isbn text,
        ... url text, year int,
        ... PRIMARY KEY (art_id)
        ... );
cqlsh:dblp> ALTER TABLE publications WITH GC_GRACE_SECONDS = 0;
cqlsh:dblp> CREATE INDEX btree_publi_type on publications(type);
```
And now lets import the data from the file `DBLP_publis.csv` :
```
cqlsh:dblp> COPY publications(art_id,type,year,title,pages_start,pages_end,booktitle,journal_series,
        ... journal_editor,journal_volume,journal_isbn,url)
        ... FROM 'DBLP/DBLP_publis.csv' WITH HEADER = true AND DELIMITER=';';
Using 7 child processes

Starting copy of dblp.publications with columns [art_id, type, year, title, pages_start, pages_end, booktitle, journal_series, journal_editor, journal_volume, journal_isbn, url].
Processed: 19693 rows; Rate:   12584 rows/s; Avg. rate:    7322 rows/s
19693 rows imported from 1 files in 0 day, 0 hour, 0 minute, and 2.690 seconds (0 skipped).
cqlsh:dblp> 
```

Let's do the same for the table `authors`, with 1 index on the `art_id` and 1 index on the `pos` :
```
cqlsh:dblp> CREATE TABLE authors (
        ... art_id TEXT, author TEXT, pos INT,
        ... PRIMARY KEY ((author), art_id)
        ... );
cqlsh:dblp> ALTER TABLE authors WITH GC_GRACE_SECONDS = 0;
cqlsh:dblp> CREATE INDEX btree_authors_art_id on authors(art_id);
cqlsh:dblp> CREATE INDEX btree_authors_pos on authors(pos);
cqlsh:dblp> COPY authors(art_id,author,pos) FROM 'DBLP/authors.csv' WITH HEADER = true AND DELIMITER=';';
Using 7 child processes

Starting copy of dblp.authors with columns [art_id, author, pos].
Processed: 50590 rows; Rate:   14771 rows/s; Avg. rate:   20546 rows/s
50590 rows imported from 1 files in 0 day, 0 hour, 0 minute, and 2.462 seconds (0 skipped).
cqlsh:dblp> 
```
Same for the `authors_publis` table :
```
cqlsh:dblp> CREATE TABLE authors_publis (
        ... art_id TEXT, author TEXT, type TEXT, title text, pages_start INT, pages_end int,
        ... booktitle text, journal_series text, journal_editor text, journal_volume int,
        ... journal_isbn text, url text, year int, pos int,
        ... PRIMARY KEY ((author), art_id)
        ... );
cqlsh:dblp> ALTER TABLE authors_publis WITH GC_GRACE_SECONDS = 0;
cqlsh:dblp> CREATE INDEX btree_authors_publi_type on authors_publis(type);
cqlsh:dblp> CREATE INDEX btree_authors_publi_title on authors_publis(title);
cqlsh:dblp> COPY authors_publis(art_id,author,type,year,title,pages_start,pages_end,booktitle,
        ... journal_series,journal_editor,journal_volume,journal_isbn,url,pos)
        ... FROM 'DBLP/authors_publis.csv' WITH HEADER = true AND DELIMITER=';';
```
But the `COPY` didn't work and we got this response :
![alt text](image.png)

The response says the errors comes from the conversion of certain values '1.0' to integer.
But rows still got imported, so lets clear the table inserts and clean the csv file on our local environment.
```
cqlsh:dblp> TRUNCATE authors_publis;
cqlsh:dblp> SELECT * FROM authors_publis LIMIT 6;

 author | art_id | booktitle | journal_editor | journal_isbn | journal_series | journal_volume | pages_end | pages_start | pos | title | type | url | year
--------+--------+-----------+----------------+--------------+----------------+----------------+-----------+-------------+-----+-------+------+-----+------

(0 rows)
cqlsh:dblp>
```
We deleted all rows from authors_publis, lets copy the `authors_publis.csv` file outside the container (from the PowerShell bash) :
```bash
docker cp cassandraServer:/DBLP/authors_publis.csv .
```
```
Successfully copied 9.72MB to C:\.......\NoSQL\NoSQL-PracticeWork-Cassandra\.
```

I wrote a [python script](./cleanup.py) that cleans the csv file by converting the `1.0` values into actual integers and write the result in a new file `authors_publis_cleaned.csv`.

I can then copy this cleaned file back into the container's **DBLP** folder :
```bash
docker cp .\authors_publis_cleaned.csv cassandraServer:/DBLP
```
```
Successfully copied 9.78MB to cassandraServer:/DBLP
```

We can then try the `COPY` command again :

```
cqlsh:dblp> COPY authors_publis(art_id,author,type,year,title,pages_start,pages_end,booktitle,
        ... journal_series,journal_editor,journal_volume,journal_isbn,url,pos)
        ... FROM '/DBLP/authors_publis_cleaned.csv' WITH HEADER = true AND DELIMITER=';';
Using 7 child processes

Starting copy of dblp.authors_publis with columns [art_id, author, type, year, title, pages_start, pages_end, booktitle, journal_series, journal_editor, journal_volume, journal_isbn, url, pos].
Processed: 50593 rows; Rate:   15298 rows/s; Avg. rate:   14393 rows/s
50593 rows imported from 1 files in 0 day, 0 hour, 0 minute, and 3.515 seconds (0 skipped).
cqlsh:dblp> 
```
And now it worked fine.

## Query Cassandra 

We succesfully created the database and imported the data from the datasets, so we can now execute queries using `Tableplus`

### Simple Queries

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

