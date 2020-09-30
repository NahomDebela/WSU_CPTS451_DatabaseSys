Authors: Nahom Y Debela, Niko N Novilla
CPTS451 - Database Systems
Instructor: Sakire Arslan Ay
Project YelpApp
2020 March 30

The YelpApp is an application that resembles the real "yelp.com" functionality. 

Note that this program requires the login information of the PostgreSQL server that you will use.
Default authentication info: dbname='yelp_db' user='postgres' host='localhost' password='password'
Update these variables to your correct server setup before attempting to run yelp_insert_v1.py.

The folder "yelp_data" is where you should extract the raw JSON data files for use by the parsing program "yelp_parse_v2.py".
This program will parse and filter the raw data; the resulting files from this process are output into the folder "yelp_output".

Extracting the Yelp data and running yelp_parse_v2.py should always be the first thing you do!
This is so the data can be properly cleaned before usage.

"TeamNN_ER_v2.pdf" contains an image of an entity-relationship (ER) model depicting our proposed database for the Yelp data.

"TeamNN_RELATIONS_v2.sql" contains our SQL "CREATE TABLE ..." statements for implementing a PostgreSQL database based 
 on the depiction of the previously mentioned ER model. 

The program "yelp_insert_v1.py" executes SQL "INSERT INTO ..." statements which will enter the parsed data into our
PostgreSQL database created by TeamNN_RELATIONS_v2.sql.

"TeamNN_UPDATE_v1.sql" holds the SQL "UPDATE ..." statements necessary to update particular count variables within the database.
 These statements must be run after insertion of the parsed data.

"milestone2_app.py" is the python file that connects to the database and populates the application. This file contains both
 python code, and SQL queries. Once this file is run, the application should be displayed.

"milestone1App.ui" This file is the user interface for our application.
We used QT Designer to design the user interface of the app.

"Yelp-BusinessApp.JPG" and "Yelp-UserApp.JPG" are pictures of the application in use.









