## Eniscope API

Best.Enegry Eniscope Analytic API access framework, which defines EniscopeAPIClient class with such functions as
 - API Authenticaton. Uses Fernet library for secure storage of user credentials in eniscope_api.conf. require credential.py with the following lines:

   encryption_key = b"XXXXXXXXXXXXXXXXXX"
   
   api_key = "xxxxxxxxxxxxxxxx"
 - base GET and Option requests
 - API user details request
 - get organizations list
 - get list of data channels belong to organization
 - get channel historical data (aka readings) for specific channel, date range, list fo metering parameters and resolution
 - get multiple channels and data ranges fo historical data simultaniously. Realy on ThreadPoolExecutor and http pooling for better performance.
 - get list of alarms related to arganization and their settings (rules and periods)
 - get alarm event list for requested organizations and data ranges

eniscopedata is a set of support classes and function to simplify work with some Eniscope specific data configurations e.g alarms etc.
