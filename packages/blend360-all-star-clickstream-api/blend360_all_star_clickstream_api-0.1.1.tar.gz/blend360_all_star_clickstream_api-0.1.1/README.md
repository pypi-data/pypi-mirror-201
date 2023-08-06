# de-allstar-training-clickstream-api
API package to request clickstream data

# Usage
`clickstream_api` module contains the class `datafetch.DataFetch`, which can be instantiated to send api requests to fetch data from an endpoint, check a job status, or query the number of visitors per day.

In order to run the `DataFetch` module you must first instantiate a `DataFetch` object. Upon your first time running the module you will be given a prompt to enter your API key. This will save your API key to your local keyring so you will not be asked for you API key again. 

## Databricks

In order to run on a databricks cluster you must first add your API key to Databricks. Copy and run the code below in your terminal to add your API key.

```shell
$ databricks secrets create-scope --scope <my-scope>
$ databricks secrets put --scope <my-scope> --key <my-key> --string-value <api_key>
```

If running on your local machine you will be prompted to enter your API key the first time running the module. The API key will be saved to your keyring.

```python
>>> from blend360_all_star_clickstream_api.datafetch import DataFetch
>>> data_fetch = DataFetch()
Enter your API Key:<api_key>
>>> 
```

If the API key needs to be removed, run [`DataFetch.deleteAPIKey()`](#clickstream_apidatafetchdatafetchdeleteapikey). If the API key needs to be updated, run [`DataFetch.updateAPIKey()`](#clickstream_apidatafetchdatafetchupdateapikey).

## `blend360_all_star_clickstream_api.datafetch.DataFetch.fetchData`
>`fetchData(self, start_date: datetime.date, end_date: datetime.date) -> str`
>
>Triggers async job that sends data to destination s3 location
>
>### Args
>
>- `start_date` (`datetime.date`): Earliest date of clickstream data to collect
>- `end_date` (`datetime.date`): Latest date of clickstream data to collect
>- `destination_bucket` (`str`): S3 bucket for data to land in
>- `destination_directory` (`str`): Directory in S3 bucket for data to land in
>- `table_name` (`str`): Name of table to fetch
>
>### Returns:
>- `requests.models.Response`:    Response object.
>
>### Example:
>```python
>>>> data_fetch.fetchData(start_date = datetime.date(2022, 1, 1), end_date = datetime.date(2023, 1, 1), destination_bucket= "clickstream-server", destination_directory = "poop_test")
><Response [200]>
>>>> data_fetch.fetchData(start_date = datetime.date(2022, 1, 1), end_date = datetime.date(2023, 1, 1), destination_bucket= "clickstream-server", destination_directory = "poop_test").json()
>{'job_id': 12345}
>>>>
>```


## `clickstream_api.datafetch.DataFetch.checkStatus`
>`checkStatus(self, job_id: int) -> str`
>
>Checks on the status of the S3 copy job
>   
>Args:
>- `job_id` (`int`): ID of S3 copy job
>    
>### Returns:
>- `requests.models.Response`:    Response object.
>
>### Example:
>```python
>>>> data_fetch.checkStatus(12345)
><Response [200]>
>>>> data_fetch.checkStatus(12345).json()
>{'execution_status': 'RUNNING'}
>>>> 
>```


## `clickstream_api.datafetch.DataFetch.updateAPIKey`
>`updateAPIKey(self)`
>
>Update the API Key
>
>### Example:
>```python
>>>> data_fetch.updateAPIKey()
>Enter your API Key:<api_key>
>>>> 
>```

## `clickstream_api.datafetch.DataFetch.deleteAPIKey`
>`deleteAPIKey(self)`
>
>Remove your API key from keyring 
>
>### Example:
>```python
>>>> data_fetch.deleteAPIKey()
>
>>>> 
>```