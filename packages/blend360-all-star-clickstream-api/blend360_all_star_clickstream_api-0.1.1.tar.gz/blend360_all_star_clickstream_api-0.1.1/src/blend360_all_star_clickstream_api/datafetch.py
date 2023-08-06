import os
import datetime
import json
from typing import Union
import warnings
from json import JSONDecodeError

import requests
import keyring
from getpass import getpass


class DataFetch():
    def __init__(self, secret_scope: str, key_name: str):
        """
        Module to interact with dataprocesing for DE All Star Project
        
        Args:
            `secret_scope` (`str`): Secrets scope to read/save secrets
            `key_name` (`str`): Name of api_key secret to read/save
        """       
        self.parse_date = lambda dt: dt.strftime('%d-%m-%Y')

        self.base_url = "https://en44bq5e33.execute-api.us-east-1.amazonaws.com/dev"

        self.header = {
            'Content-Type': 'application/json'
        }

        self.api_key_service_name = secret_scope
        self.api_key_username = key_name

        self.on_databricks = self._is_on_databricks()
        if self.on_databricks:
            from pyspark.sql import SparkSession
            from pyspark.dbutils import DBUtils
            self.spark = SparkSession.builder.getOrCreate()
            self.dbutils = DBUtils(self.spark)

        self._set_api_key()


    def _is_on_databricks(self) -> bool:
        """
        Check if currently running on Databricks Returns:
            
        Returns:
            `bool`:   `True` if running on databricks
                       Otherwise `False`
        """
        return "DATABRICKS_RUNTIME_VERSION" in os.environ


    def _set_api_key(self):
        """
        Set the api_key in system keyring for retrieval.  
        If api_key is already set from previous session then this key will be loaded.
        api_key can be reset using the method `updateApiKey()`      
        """
        if (not self.on_databricks) and (self._get_api_key() is None):
            self.updateAPIKey()

            
    def _get_api_key(self) -> str:
        """
        Method to programmatically access api key from secure keyring        
        
        Returns:
            `str`: api key
        """
        if self.on_databricks:
            return self.dbutils.secrets.get(self.api_key_service_name, self.api_key_username)
        else:
            return keyring.get_password(self.api_key_service_name, self.api_key_username)


    def updateAPIKey(self):
        """
        Update the API Key      
        """
        if self.on_databricks:
            warnings.warn("WARNING: API Keys cannot be programmatically updated on Databricks. No updates will be made.", UserWarning)
        else:
            keyring.set_password(
                self.api_key_service_name, 
                self.api_key_username, 
                getpass("Enter your API Key:"))


    def deleteAPIKey(self):
        """
        Remove your API key from keyring        
        """
        if self.on_databricks:
            warnings.warn("WARNING: API Keys cannot be programmatically deleted on Databricks. No secrets will be deleted.", UserWarning)
        else:
            keyring.delete_password(self.api_key_service_name, self.api_key_username)


    def fetchData(self, 
                  start_date: datetime.date, 
                  end_date: datetime.date, 
                  destination_bucket: str, 
                  destination_directory: str,
                  table_name: str) -> requests.models.Response:
        """
        Triggers async job that sends data to destination s3 location
        
        Args:
            `start_date` (`datetime.date`): Earliest date of clickstream data to collect
            `end_date` (`datetime.date`): Latest date of clickstream data to collect
            `destination_bucket` (`str`): S3 bucket for data to land in
            `destination_directory` (`str`): Directory in S3 bucket for data to land in
            `table_name` (`str`): Name of table to fetch

        Returns:
            `requests.models.Response`:    Response object.
        """
        url = os.path.join(self.base_url, "fetch_data")
        
        payload = json.dumps({
            "api_key": self._get_api_key(),
            "start_date": self.parse_date(start_date),
            "end_date": self.parse_date(end_date),
            "destination_s3_bucket": destination_bucket,
            "destination_s3_directory": destination_directory,
            "table": table_name
        })

        response = requests.post(url, headers = self.header, data = payload)
        
        return response
        

    def checkStatus(self, job_id: str) -> dict:
        """
        Checks on the status of the S3 copy job
        
        Args:
            `job_id` (`str`): ID of S3 copy job
        
        Returns:
            requests.models.Response:    Response object.
        """
        url = os.path.join(self.base_url, "job_status")

        payload = json.dumps({
            "api_key": self._get_api_key(),
            "job_id": job_id
        })

        response = requests.get(url, headers = self.header, data = payload)
        
        return response
    