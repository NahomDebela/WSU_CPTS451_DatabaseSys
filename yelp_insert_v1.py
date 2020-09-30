import psycopg2
import csv

# These strings are the output paths for each CSV output file from yelp_parse.py - all single variables are ready to be inserted, but list variables require an extra cleaning step.
OUTPUT_BUSINESS = "yelp_output\yelp_business_output.csv"
OUTPUT_CHECKIN = "yelp_output\yelp_checkin_output.csv"
OUTPUT_TIP = "yelp_output\yelp_tip_output.csv"
OUTPUT_USER = "yelp_output\yelp_user_output.csv"

# This string contains the authentication info for the PostgreSQL database. If you plan on sharing this program, make sure to reset this info beforehand.
AUTH_INFO = "dbname='yelp_db' user='postgres' host='localhost' password='HollowKn1ght!5598'"

# This helper function replaces problematic characters in strings that are derived from list variables, making the output statement much easier to work with.
def clean_string(s):
    return s.replace("[", "").replace("]", "").replace(" '", "").replace("'", "")

def insert_business():
    with open(OUTPUT_BUSINESS, "r") as business:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(business)
        next(line)
        i = 1
        
        for row in line:
            data = ", ".join(row).split(", ")
            insert = "INSERT INTO Business (business_id, name, city, state, postal_code, address, is_open, numCheckins, numTips, latitude, longitude, stars, review_count)\n" + \
                     "VALUES ('" + data[0] + "','" + data[1] + "','" + data[3] + "','" + data[4] + "','" + data[5] + "','" + data[2] + "','" + data[10] + "','0','0','" + data[6] + \
                     "','" + data[7] + "','" + data[8] + "','" + data[9] + "');"
            data = ""
            
            try:
                cursor.execute(insert)
            except:
                print("ERROR: Insertion failed to execute.")
                return
            connection.commit()
            i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} business instances from \"{}\"".format(i, OUTPUT_BUSINESS))

def insert_categories():
    with open(OUTPUT_BUSINESS, "r") as categories:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(categories)
        next(line)
        i = 1
        
        for row in line:
            data = [row[0]]
            
            for x in range(11, len(row)):
                data.append(clean_string(row[x]))
            
            for y in range(1, len(data)):
                insert = "INSERT INTO Categories (business_id, category_name)\n" + \
                         "VALUES ('" + data[0] + "','" + data[y] + "');"
                try:
                    cursor.execute(insert)
                except:
                    print("ERROR: Insertion failed to execute.")
                    return
                connection.commit()
                i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} category instances from \"{}\"".format(i, OUTPUT_BUSINESS))

def insert_checkin():
    with open(OUTPUT_CHECKIN, "r") as checkin:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(checkin)
        next(line)
        i = 1
        
        for row in line:
            data = [row[0]]
            
            for x in range(1, len(row)):
                data.append(clean_string(row[x]))
            
            for y in range(1, len(data)):
                insert = "INSERT INTO Checkin (business_id, date)\n" + \
                         "VALUES ('" + data[0] + "','" + data[y] + "');"
                try:
                    cursor.execute(insert)
                except:
                    print("ERROR: Insertion failed to execute.")
                    return
                connection.commit()
                i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} check-in instances from \"{}\"".format(i, OUTPUT_TIP))

def insert_friend():
    with open(OUTPUT_USER, "r") as friend:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(friend)
        next(line)
        i = 1
        
        for row in line:
            data = [row[0]]
            
            for x in range(9, len(row)):
                data.append(clean_string(row[x]))
            
            for y in range(1, len(data)):
                if data[y] == "":
                    break
                
                insert = "INSERT INTO Friend (user_id, friend_id)\n" + \
                         "VALUES ('" + data[0] + "','" + data[y] + "');"
                try:
                    cursor.execute(insert)
                except:
                    print("ERROR: Insertion failed to execute.")
                    return
                connection.commit()
                i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} friend instances from \"{}\"".format(i, OUTPUT_USER))

def insert_tip():
    with open(OUTPUT_TIP, "r") as tip:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(tip)
        next(line)
        i = 1
        
        for row in line:
            data = ", ".join(row).split(", ")
            insert = "INSERT INTO Tip (business_id, date, likes, text, user_id)\n" + \
                     "VALUES ('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] + "','" + data[4] + "');"
            data = ""
            
            try:
                cursor.execute(insert)
            except:
                print("ERROR: Insertion failed to execute.")
                return
            connection.commit()
            i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} tip instances from \"{}\"".format(i, OUTPUT_TIP))

def insert_user():
    with open(OUTPUT_USER, "r") as user:
        try:
            connection = psycopg2.connect(AUTH_INFO)
        except:
            print("ERROR: Unable to connect to PostgreSQL database.")
            return
        cursor = connection.cursor()
        
        line = csv.reader(user)
        next(line)
        i = 1
        
        for row in line:
            data = ", ".join(row).split(", ")
            insert = "INSERT INTO Users (user_id, totalLikes, latitude, longitude, yelping_since, name, tip_count, average_stars, useful, funny, cool, fans)\n" + \
                     "VALUES ('" + data[0] + "','0','0','0','" + data[2] + "','" + data[1] + "','" + data[7] + "','" + data[3] + "','" + data[6] + "','" + \
                     data[5] + "','" + data[4] + "','" + data[8] + "');"
            data = ""
            
            try:
                cursor.execute(insert)
            except:
                print("ERROR: Insertion failed to execute.")
                return
            connection.commit()
            i += 1
        
        cursor.close()
        connection.close()
    
    print("- Inserted {} user instances from \"{}\"".format(i, OUTPUT_USER))



#insert_business()
#insert_categories()
insert_checkin()
#insert_user()
#insert_friend()
#insert_tip()


