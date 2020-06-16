# Rentals.ca API document.

##Summary
- Great datas related to rent price for apartments / condos
- Very weak for room rents or student housing

###Common API endpoint

#### GET

https://rentals.ca/phoenix/api/v1.0.1/listings?obj_path=CITY_NAME

**params**
- details ?
- suppress-pagination ?
- limit
  - 500 is max
- obj_path
  - city-name
- bbox
  - bottom left long, bottom left lat, top right long, top right lat 
- types[]
  - room, etc.

ex) returned JSON format (Only important ones.)
- meta
  - total_properties
  - returned_properties
- data
  - cities
  - listings[]
    - beds_range
    - location
    - property_type
    - rent_range
    - updated

### Supported City Names

https://rentals.ca/ontario
mostly, naming convention is kebab case.

### Scope

#### GTA (Toronto, York, Ryerson, etc.)

- toronto
- york
- east-york
- etobicoke
- markham
- mississauga
- north-york
- scarborough
- richmond-hill
- oakville
- brampton

#### London (Western, Fanshawe)

- london

#### Waterloo (Laurier, Waterloo)

- Waterloo
- Kitchener

#### Hamilton Area (McMaster)

- hamilton
- burlington