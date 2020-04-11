**Vehicle Routing Problem (using Google OR Tools, Bing Maps API)**


The given code is for making a simple API based Vehicle Routing Problem Solver using Google OR ToolsThe program uses flask+gunicorn for creating the API.

Installation :


1) Run setup.sh for downloading all the required python libraries using pip 
2) Run run.sh for running the gunicorn server at 0.0.0.0:8080
3) Go to 0.0.0.0:8080 and upload the csv file in the required format


The API could also be queried using POST multipart/form-data requests at 0.0.0.0:8080/handleUpload

The proclfile has also been attached so that one could directly upload the app on heroku

Note : The application uses Bing Free API for calculating the distance matrix the key should be provided in the key file (currently has nothing) . Make sure to register for a Bing Free API and add the key in the key file before starting the server.

My heroku-application : https://vehicleroutingproblem.herokuapp.com/

Note : Since the heroku-application runs on free-tier program hence takes 20 seconds to boot up from inactivity (of 30 min) 
 
