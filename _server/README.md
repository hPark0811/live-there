# LiveThere - Backend

***Do not push your virtual env setting to this repo, as it will pollute the repository***

#### Commands

`python3 -m venv env`

On Windows, run:
`env\Scripts\activate.bat`

On Unix or MacOS, run:
`source env/bin/activate`

Then
`pip install -r requirements.txt`


#### Deployment
##### You must have gcloud SDK installed to deploy through CLI

To select project (only need to be done once)
`gcloud init`

run following command
`gcloud app deploy`

to check if the deployment has been done properly
`gcloud app browse`
