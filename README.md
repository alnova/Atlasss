Django install running on google app engine (GAE)

(A) To get started as a developer, install the Google cloud SDK https://developers.google.com/appengine/docs/python/gettingstartedpython27/devenvironment

curl sdk.cloud.google.com | bash

From your terminal, clone the git repo. git clone https://github.com/kariefury/assa.git

To login to Assailed each time: sign into google cloud

gcloud auth login

Project assa

...programming happens...

test it locally...(Note... you have to be outside of assa directory)

dev_appserver.py assa

...everything works...

appcfg.py -A space-moon-111 update assa (Once again, be outside of assa directory)
