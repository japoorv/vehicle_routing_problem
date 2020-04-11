The given code is for making a simple API based Vehicle Routing Problem Solver using Google OR ToolsThe program uses flask+gunicorn for creating the API.

Installation :
1) Run setup.sh for downloading all the required python libraries using pip 
2) Run run.sh for running the gunicorn server at 0.0.0.0:8080
3) Go to 0.0.0.0:8080 and upload the csv file in the required format


The API could also be queried using POST multipart/form-data requests at 0.0.0.0:8080/handleUpload

The proclfile has also been attached so that one could directly upload the app on heroku 
