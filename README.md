# bigQueryExporter
Export query data from google bigquery to local machine

#### Example
    from bigQueryExport import BigQueryExporter
    bigQueryExporter = BigQueryExporter(project_name, dataset_name, bucket_name)
    bigQueryExporter = query_to_local(query, job_name, '../data')
