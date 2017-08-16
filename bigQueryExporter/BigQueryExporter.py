import os
import time
import uuid
import logging
import shutil
from datetime import datetime 
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.dataset import Dataset


class BigQueryExporter:
    def __init__(self, project_name, dataset_name, bucket_name):
        self.project_name = project_name
        self.dataset_name = dataset_name
        self.bucket_name = bucket_name
        
        self.bigquery_client = bigquery.Client(project=project_name)
        self.storage_client = storage.Client(project=project_name)
        
        
    def query_to_table(self, query, job_name):
        #logging
        logging.info('[BigQueryExporter] ['+job_name+'] ::query_to_table start')
        startTime= datetime.now()
        
        # initialize variables
        dataset_name = self.dataset_name
        bigquery_client = self.bigquery_client
        
        # Point to the dataset and table
        destination_dataset = Dataset(dataset_name, bigquery_client)
        destination_table = Table(job_name, destination_dataset)

        # Create an empty table
        if destination_table.exists():
            destination_table.delete()
        destination_table.create()
        
        # Execute the job and save to table
        unique_id = str(uuid.uuid4())
        job = bigquery_client.run_async_query(unique_id, query)
        job.allow_large_results = True
        job.destination = destination_table
        job.begin()
        
        # Wait till the job done
        while not job.done():
            time.sleep(1)
        
        # logging
        timeElapsed=datetime.now()-startTime 
        logging.warning('[BigQueryExporter] ['+job_name+'] ::query_to_table completed, elpased {}s'.format(timeElapsed.seconds))
        
        return destination_table
        
        
    def table_to_gs(self, destination_table, job_name):
        #logging
        logging.info('[BigQueryExporter] ['+job_name+'] ::table_to_gs start')
        startTime= datetime.now()
        
        # initialize variables
        bigquery_client = self.bigquery_client
        storage_client = self.storage_client
        bucket_name = self.bucket_name
        
        # Create empty folder
        bucket = storage_client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=job_name))
        for blob in blobs:
            blob.delete()
        
        # Execute the job and save to google storage
        unique_id = str(uuid.uuid4())
        file_destination = 'gs://' +bucket_name+ '/' +job_name+ '/out-*.csv'
        job = bigquery_client.extract_table_to_storage(unique_id, destination_table, file_destination)
        job.begin()
        
        # Wait till the job done
        while not job.done():
            time.sleep(1)
            
        # logging
        timeElapsed=datetime.now()-startTime 
        logging.warning('[BigQueryExporter] ['+job_name+'] ::table_to_gs completed, elpased {}s'.format(timeElapsed.seconds))
        
        return bucket
            
            
    def gs_to_local(self, bucket, job_name, data_dir_path):
        #logging
        logging.info('[BigQueryExporter] ['+job_name+'] ::gs_to_local start')
        startTime= datetime.now()
        
        # initialize variables
        dir_path = data_dir_path + '/' + job_name
        
        # Point to the folders in google storage
        blobs = list(bucket.list_blobs(prefix=job_name))
        
        # Create empty folder
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        
        # Export the files in google storage to local
        for blob in blobs:
            name = blob.name.split('/')[-1]
            blob.download_to_filename(dir_path+ '/' + name)
        
        # logging
        timeElapsed=datetime.now()-startTime 
        logging.warning('[BigQueryExporter] ['+job_name+'] ::gs_to_local completed, elpased {}s'.format(timeElapsed.seconds))
        
        
    def query_to_local(self, query, job_name, data_dir_path):
        #logging
        logging.info('[BigQueryExporter] ['+job_name+'] ::query_to_local start')
        startTime= datetime.now()
        
        destination_table = self.query_to_table(query, job_name)
        bucket = self.table_to_gs(destination_table, job_name)
        self.gs_to_local(bucket, job_name, data_dir_path)
        
        # logging
        timeElapsed=datetime.now()-startTime 
        logging.warning('[BigQueryExporter] ['+job_name+'] ::query_to_local completed, elpased {}s'.format(timeElapsed.seconds))