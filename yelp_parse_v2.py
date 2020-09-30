import json

# The following strings are the filepaths for their corresponding JSON data files. Set these to their correct paths before running!
FILEPATH_BUSINESS = "yelp_data\yelp_business.JSON"
FILEPATH_CHECKIN = "yelp_data\yelp_checkin.JSON"
FILEPATH_TIP = "yelp_data\yelp_tip.JSON"
FILEPATH_USER = "yelp_data\yelp_user.JSON"

# These strings are the output paths for each CSV output file.
OUTPUT_BUSINESS = "yelp_output\yelp_business_output.csv"
OUTPUT_CHECKIN = "yelp_output\yelp_checkin_output.csv"
OUTPUT_TIP = "yelp_output\yelp_tip_output.csv"
OUTPUT_USER = "yelp_output\yelp_user_output.csv"

# These last strings are the headers for each CSV output file.
HEADER_BUSINESS = "business_id,name,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,categories"
HEADER_CHECKIN = "business_id,date"
HEADER_TIP = "business_id,date,likes,text,user_id"
HEADER_USER = "user_id,name,yelping_since,average_stars,cool,funny,useful,tipcount,fans,friends"

# This helper function replaces any problematic characters in strings, making the output files much easier to work with.
def clean_string(s):
    return s.replace("'", "`").replace("\"", "`").replace("\n", " ").replace(",", "")

def parse_business():
    with open(FILEPATH_BUSINESS, "r") as business:  # Prepare the data file (this one is for yelp_business, so use the filepath for business)
        file = open(OUTPUT_BUSINESS, "w")           # Open the output file...
        file.write(HEADER_BUSINESS + "\n")          # ...and write the header
        line = business.readline()                  # Then start the parsing process by readying the line
        i = 0                                       # Counter variable for the optional concluding print statement
        
        while line:
            # Load the first line of the data file
            data = json.loads(line)
            
            # Retrieve business_id, name, address, city, and state
            file.write(clean_string(data["business_id"]) + ",")
            file.write(clean_string(data["name"]) + ",")
            file.write(clean_string(data["address"]) + ",")
            file.write(clean_string(data["city"]) + ",")
            file.write(clean_string(data["state"]) + ",")
            file.write(clean_string(data["postal_code"]) + ",")
            
            # Retrieve latitude, longitude, stars, and review count; these are presented as numerical values, but can be safely treated as strings
            file.write(str(data["latitude"]) + ",")
            file.write(str(data["longitude"]) + ",")
            file.write(str(data["stars"]) + ",")
            file.write(str(data["review_count"]) + ",")
            
            # Retrieve open state; this variable is a boolean represented as "1" or "0"
            if data["is_open"]:
                file.write("1,")
            else:
                file.write("0,")
            
            # Retrieve categories; this is just a list that can be extracted directly
            categories = data["categories"].split(", ")
            file.write(str(categories))
                        
            # Done with the line! Just cap it off with a new-line character, ready the next line, and increment the counter
            file.write("\n")
            line = business.readline()
            i += 1
        
        # Once this file is complete, just close em up
        file.close()
        business.close()
        
        # Optional conclusion print statement
        print("- Parsed through {} instances in \"{}\"".format(i, FILEPATH_BUSINESS))

def parse_checkin():
    with open(FILEPATH_CHECKIN, "r") as checkin:
        file = open(OUTPUT_CHECKIN, "w")
        file.write(HEADER_CHECKIN + "\n")
        line = checkin.readline()
        i = 0
        
        while line:
            data = json.loads(line)
            
            file.write(clean_string(data["business_id"]) + ",")
            
            date = data["date"].split(",")
            file.write(str(date))
            
            file.write("\n")
            line = checkin.readline()
            i += 1
        
        file.close()
        checkin.close()
        
        print("- Parsed through {} instances in \"{}\"".format(i, FILEPATH_CHECKIN))

def parse_tip():
    with open(FILEPATH_TIP, "r") as tip:
        file = open(OUTPUT_TIP, "w")
        file.write(HEADER_TIP + "\n")
        line = tip.readline()
        i = 0
        
        while line:
            data = json.loads(line)
            
            file.write(clean_string(data["business_id"]) + ",")
            file.write(clean_string(data["date"]) + ",")
            file.write(str(data["likes"]) + ",")
            file.write(clean_string(data["text"]) + ",")
            file.write(clean_string(data["user_id"]))
            
            file.write("\n")
            line = tip.readline()
            i += 1
        
        file.close()
        tip.close()
        
        print("- Parsed through {} instances in \"{}\"".format(i, FILEPATH_TIP))

def parse_user():
    with open(FILEPATH_USER, "r") as user:
        file = open(OUTPUT_USER, "w")
        file.write(HEADER_USER + "\n")
        line = user.readline()
        i = 0
        
        while line:
            data = json.loads(line)
            
            file.write(clean_string(data["user_id"]) + ",")
            file.write(clean_string(data["name"]) + ",")
            file.write(clean_string(data["yelping_since"]) + ",")
            
            file.write(str(data["average_stars"]) + ",")
            file.write(str(data["cool"]) + ",")
            file.write(str(data["funny"]) + ",")
            file.write(str(data["useful"]) + ",")
            file.write(str(data["tipcount"]) + ",")
            file.write(str(data["fans"]) + ",")
            
            friends = data["friends"]
            file.write(str(friends))
            
            file.write("\n")
            line = user.readline()
            i += 1
        
        file.close()
        user.close()
        
        print("- Parsed through {} instances in \"{}\"".format(i, FILEPATH_USER))



#   #   #

parse_business()
parse_checkin()
parse_tip()
parse_user()

print("All parse processes completed. Check the \"yelp_output\" folder for all output files.")

#   #   #


