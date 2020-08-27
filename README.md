# <img src="_client/livethere-app/src/assets/LiveThereLogo.png" alt="LiveThere" width="160" height="35">

LiveThere is a cost of living analysis & budgeting website for highschool students, where students can view their most up to date estimated cost of living based on the selected post-secondary institution. 

* **20,000+ data points** collected through web scraping to provide analysis (rental, eating out, utilities, etc.).
* **Accurate** cost of living analysis with following query options.
  * **Rental**: # of bedrooms, # of bathrooms, property type, distance from campus
  * **Utilities**: Electrical, gas, water, etc.
  * **Eating out**: Retaurant type, has patio etc.
* **Compatible** with devices of all sizes and all Operating Systems and browsers.

## Tech Stack
<div style="text-align: center">
  <img src="_client/livethere-app/src/assets/Stack Diagram.png">
</div>

### DB Design
<div style="text-align: center">
  <img src="_client/livethere-app/src/assets/DB Class Diagram.png" width="70%">
</div>

#### Behind the Scene
* **Frontend**
  * **Redux** for application state management.
  * **Material UI** theme to provide common theme throughout the user experience.
* **Backend**
  * **Cache** utilized to minimize db query.
  * **Normalized** relational database to minimize redundancy and ensure only related data is stored in each table.
* **Frontend**
  * **Figma** for UI/UX design

## Demo
Working live demo:  https://live-there-281716.firebaseapp.com/



