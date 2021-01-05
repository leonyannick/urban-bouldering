# Nuremberg Bouldering Map
#### Video Demo:  https://youtu.be/00H4BfG4gJI
#### Description:
My project is an interactive map of Nuremberg and the surrounding area where users are able to create markers where they find spots for climbing, mostly bouldering.
Users are able to create an account and log in to the Website.

Breakdown:
The framwork for registering and logging in users and saving their data in a sql database is mostly reused from the finance problem set.

index.html:
The index page has an open street map tile embedded with the leaflet api and shows the city of Nuremberg and its surrounding area. I choose open street map as opposed to google map because it is open source.
Users are able to create markers by clicking anywhere on the map.
The map is embedded so that it is also user friendly on mobile.
A HTML form opens up at the respective location and users can input a name, a grade (difficulty), a description, and upload a photo of the climb.
For uploading the images I used flask documenation for uploading files. I only allow users to upload some image file extensions to prevent wrong use.
There is as flask function calles secure_filename() which further makes sure that the uploaded file is legitimate.
Markers that were already created (both by the respective user and others too) are also displayed on the map.
Clicking on them opens a small popup with information and the thumbnail image and a link that opens all the information about the boulder in a new tab.

boulder_fullscreen.html:
The new tab that is opened displays all the information about the climb including the description and a much bigger version of the image.
There is also a button showing you exactly where the boulder is located on the map.

history.html:
Furthermore there is an option to view all boulders that have been added inside of a table by all users.
All boulders can be sorted either by name, grade or date by clicking on the header of the respective column.
They are sorted by a javascript function which I found at w3schools website (https://www.w3schools.com/howto/howto_js_sort_table.asp).
By clicking on the name of the boulder the respective boulder_fullscreen.html opens up.

All information about the boulders is stored inside a sqlite database inside a table called "boulder". The images that can be uploaded by users are saved in a separate images directory.
To avoid pictures being overwritten by pictures with the same name, they get renamed to the corresponding name of the boulder which is tested to be unique.
They are not stored directly in the database, because these images are usually larger in size and this would slow down the website.
Therefore only the path to the images is stored inside the database.

Features I want to add/improve:
-adding a button on the map to access the current location of the user
-optimization for mobile
-edit/delete boulders
-improve the appearance of the website
-linking the accounts to an email adress, so that users can reset their password
-annotate images, so climbers can cleary distinguish between boulders