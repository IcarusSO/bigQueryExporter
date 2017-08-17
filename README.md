# bigQueryExporter
Export query data from google bigquery to local machine

#### Installation
    pip install bigQueryExporter
    pip3 install bigQueryExporter

#### Example
    from bigQueryExport import BigQueryExporter
    bigQueryExporter = BigQueryExporter(project_name, dataset_name, bucket_name)
    bigQueryExporter = query_to_local(query, job_name, '../data')

#### Requirement
- Your server/ local machine should have the right to access the project
- Right should be granted following the insturction on [Google SDK](https://cloud.google.com/sdk/docs/)
- Execute the following command

    gcloud auth application-default login
