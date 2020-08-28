import pymysql, os, json

# read JSON file which is in the next parent folder

# Change file to your location, run yelp api first and save json in file
file = '/Users/saminouralla/Desktop/restaurantData.json'


json_data=open(file).read()
json_obj = json.loads(json_data)

#print(json_obj)

# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            for x in val:
               print(x)
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host = '35.225.74.52',user = 'root',passwd = 'livethere2020',db = 'livethere')
cursor = con.cursor()


# parse json data to SQL insert
for i, item in enumerate(json_obj):
    print(item)
    
    yelpID = validate_string(item.get("id",None))
    price = validate_string(item.get("price",None))
    rating = validate_string(item.get("review_count",None))
    cursor.execute("INSERT INTO YelpScehma (businessId,	priceLevel,	ratingCount) VALUES (%s,%s,%s)", (yelpID,price,rating))

con.commit()
con.close()