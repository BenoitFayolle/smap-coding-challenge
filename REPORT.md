## Documentation

* Check required packages in requirements.txt
* use the command "python manage.py import <path_to_data_folder>" to import your data in the application database. The data folder should contain:
	* a user_data.csv file 
	id | area | tariff
	---|------|-------
	1 | a1 | t1
	2 | a1 | t2
	3 | a2 | t3
	... | ... | ...
	* a "consumption" directory with file names <id.csv> containing the consumption data in the following form
	datetime | consumption
	---------|------------
	2016-07-01 00:00:00 | 100.
	2016-07-01 00:30:00 | 130.
	2016-07-01 01:00:00 | 90.
	... | ...
* once all the user data has been imported, you can run the server.
* if new data is to be added, flush the database first with "python manage.py flush" command and use the import.py command on the new data folder.

* There are two views in the app:
	* the summary view '/' or '/summary/': Presents the aggregation of consumption under two bargraphs, average and total consumption
	* the detail view '/detail/<user_id>' : Presents the consumption time series for the specified <user_id>.
	
## Remarks
* The import.py command is at its first development stage. It works only once because it doesn't check for redundancy at all. If new users and/or consumption data is added to the data folder, it is necessary to flush the database first. Further development would include 
	* redundancy check of data to be pushed.
	* making our app modifiable by the admin or an user, to allow the importation of data in a more user-friendly way.
* I chose to add the mean_consumption and total_consumption fields to the 'user' model to make it quick to access for the summary view. The trade-off is off course redundancy in the database and lower normal form.
* Summary view: further development could include
	* ability to view the area and tariff variable through variable colors on the bargraph
	* hyperlink to detail views on user ids in the table
* I made the assumption that the area and tariff values had (a1,a2) and (t1,t2,t3) respectively as only possible values. And that others user files could be added in the future. Hence I use an "ENUM" type of field for area and tariff.
* The time zone is has to be specified. I had no specification on the origin of the data so I arbitrarily left it at UTC.
* Tests: No testcase was created but the following code was executed on the command line to ensure every detail views were successfully generated:
```
	from django.test.utils import setup_test_environment
	from django.test import Client
	from consumption.models import user
	setup_test_environment()
    client = Client()
    for u in user.objects.all():
        print(client.get('/detail/' + str(u.user_id)).status_code)
```
