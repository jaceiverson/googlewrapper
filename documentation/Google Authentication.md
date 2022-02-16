# Establish your Connection
## Option 1 - Assign Connection Variable
Use the Connection class found in connect.py to assign credentials. It is recomended to do this if you want to use a credentials file that is: 

1) not in the CWD 

OR 

2) not named "client_secret.json". 

'client_secret.json' should be in the working directory, if not, please declare the path while initializing the class. See the example below for both versions.
```py
from googlewrapper.connect import Connection

# in working directory
google_connection = Connection()

# declare path in class
google_connection = Connection("file/path/to/client_secret.json")
```

Once we have our connection object, we will need to declare the scope of our access. You can do this by accessing the following class methods:

| Google Service       | Module     | Authentication Type | Credential File |
| :------------- | :----------: | :----------: | :----------: |
|  Analytics | .ga()   | oAuth | client_secret.json | 
| Search Console   | .gsc() | oAuth |  client_secret.json | 
| Calendar   | .cal() | oAuth | client_secret.json | 
| Big Query   | .gbq() | Service Account | gbq-sa.json |
| PageSpeed  | n/a | API Key | n/a | 
| Gmail   | .gmail() | oAuth | client_secret.json | 
| Sheets   | .gs() | oAuth | client_secret.json | 

Note, you can change the file path for authenticating Google Big Query by passing in the Service Account json in the gbq method

```py
gbq_connection = Connection().gbq("file/path/to/service_account.json")
```

## Option 2 - Default Connection (One Line Connect) - Generally Reccomended
It is possible to just use one line when connecting. It is recommended to do this if you will not need your authentication object, and will just be using the wrapper class.  

This can be done by initializing the wrapper classes, without any arguments. By default, each class will authenticate with the default method found in the connect class. 

__IMPORTANT__: To do this, we must have 'client_secret.json' in our working directory. -- for GBQ your 'gbq-sa.json' must be in the working directory

See below
```py
from googlewrapper.gsc import GoogleSearchConsole

gsc = GoogleSearchConsole()
```
## Post Authentication - Stored Credentials
After authentication has taken place (via either option), a folder will be created in your cwd named _credentials_. The respective authentication scopes will be stored there so you don't have to authenticate every time. Each token is stored with the Google property name as a .dat file.
 