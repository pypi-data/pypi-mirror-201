# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['awsdf']

package_data = \
{'': ['*']}

install_requires = \
['awswrangler>=2.14.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'awsdf',
    'version': '0.1.10',
    'description': 'AWS metadata as dataframes',
    'long_description': '\nawsdf package\n*************\n\n\nSubmodules\n==========\n\n\nawsdf.aws module\n================\n\nThis module enables connecting to AWS and extracting metadata in\npandas dataframes.\n\n**Installing from PyPI:** *pip install -U awsdf*\n\n**USAGE:**\n\n   import awsdf\n\n   aws_account = awsdf.Account(profile_name=”<PROFILE_NAME>”)\n\n   glue_databases_df = aws_account.glue_get_databases()\n\n**class awsdf.aws.Account(aws_access_key_id=None,\naws_secret_access_key=None, aws_session_token=None, region_name=None,\nprofile_name=None)**\n\n   Instantiate class object for connecting to AWS and retriving\n   metadata from AWS\n\n   **__init__(aws_access_key_id=None, aws_secret_access_key=None,\n   aws_session_token=None, region_name=None, profile_name=None)**\n\n      Provide access keys OR Profile name to connect to AWS account.\n      Keys take preceedence\n\n      **Parameters:**\n\n         *aws_access_key_id (string) – AWS access key ID*\n\n         *aws_secret_access_key (string) – AWS secret access key*\n\n         *aws_session_token (string) – AWS temporary session token*\n\n         *region_name (string) – AWS region*\n\n         *profile_name (string) – AWS profile name*\n\n   **glue_get_jobs() -> DataFrame**\n\n      Get AWS Glue jobs\n\n      Returns:\n         dataframe\n\n   **glue_get_job_history(job_name, no_of_runs=1) -> DataFrame**\n\n      Retrieve glue job history\n\n      Arguments:\n         job_name – Name of job to retrive history\n\n      Keyword Arguments:\n         no_of_runs – No of runs to retrive in descending order\n         (default: {1})\n\n      Returns:\n         dataframe\n\n   **glue_get_databases() -> DataFrame**\n\n      Get AWS Glue jobs\n\n      Returns:\n         dataframe\n\n   **glue_get_tables(dbname=None) -> DataFrame**\n\n      Get AWS Glue tables\n\n      Keyword Arguments:\n         dbname – Database Name for which to retrieve tables (default:\n         {None})\n\n      Returns:\n         dataframe\n\n   **glue_get_fields(dbname, tablename) -> DataFrame**\n\n      Get AWS Glue table columns\n\n      Keyword Arguments:\n         dbname – Database Name for table  tablename – Database Name\n         for which to retrieve columns\n\n      Returns:\n         dataframe\n\n   **athena_data_dictionary(skip_dbs: list = []) -> DataFrame**\n\n      Get AWS Athean data dictionary. A data frame with all databases,\n      tables & fields with datatypes\n\n      Keyword Arguments:\n         skip_dbs (optional) – list of databases to be skiped\n\n      Returns:\n         dataframe\n\n\nModule contents\n===============\n',
    'author': 'Allan',
    'author_email': 'allan.dsouza@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
