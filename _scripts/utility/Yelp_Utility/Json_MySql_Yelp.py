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
for i, item in enumerate(json_obj.get('businesses')):
    #print(item)    
    yelpID = validate_string(item.get("id",None))
    price = validate_string(item.get("price",None))
    postal = validate_string(item.get("location",None).get("zip_code",None))
    
    latitude = item.get("coordinates",None).get("latitude",None)
    longitude = item.get("coordinates",None).get("longitude",None)
    rating = item.get("review_count",None)
    
    cursor.execute(
        "INSERT INTO Restaurant (yelpId,priceLevel,postalCode,ratingCount,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s)", 
    (yelpID,price,postal,rating,latitude,longitude))

con.commit()
con.close()