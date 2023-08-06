# Metis Flask SQLAlchemy log collector

### About
This library logs the HTTP requests created by Flask and SQLAlchemy with the SQL commands they generate. The library can also collect the execution plan for deeper analysis.

The log records stored in a local file. Future versions will allow saving the log records directly to log collectors such as DataDog, Logz.io and Splunk.

The log can be analyzed using our [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=Metis.dba-ai-vscode)

### Technical

This library uses [OpenTelemetry](https://pypi.org/project/opentelemetry-sdk/) to instrument both Flask and SQLAlchemy.

Tested on python 3.8.9, Flask 2.1.1, SQLAlchemy 1.4.33, PostgreSQL 12 or higher.

### Instrumentation
Installation:
```bash
pip install sqlalchemycollector
```
Instrumentation:

* Configure the destination file name

* Configure logging the execution plan

By default the package only logs the SQL commands and the estimated execution plan (PlanCollectType.ESTIMATED).

The library:

1. Logs the estimated execution plan by running the SQL command using
    ```sql
    EXPLAIN ( VERBOSE, COSTS, SUMMARY, FORMAT JSON)
    ```
2. Runs the SQL command.

Logging the estimated plan has an impact on performances but usually, in a dev environment who doesn't run a large number of SQL commands, the impact is very low, around 3%.

Warning! Do NOT run the code in Production! An environment variable should prevent the package from collecting the estimated execution plan  in Production.

The library can be configured using PlanCollectType.NONE to log only the SQL Commands while the execution plans, estimated or actual, will be calculated later using our platform.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemycollector import setup, MetisInstrumentor, PlanCollectType

# existing app initialization
app = Flask(...)
db = SQLAlchemy(app)

# By default, the package logs the SQL commands and their execution plan. 
# It can also be configured manually to collect only the SQL commands using PlanCollectType.NONE. 
# We recommend collecting the estimated plan too.
optional_plan_collect_type = PlanCollectType.ESTIMATED

# To start collecting the logs:
instrumentation: MetisInstrumentor = setup('<SERVICE_NAME>',
                                           api_key='<API_KEY>',
                                           service_version='<SERVICE_VERSION>' #optional
                                           ) 


instrumentation.instrument_app(app, db.get_engine())
```
### Exclude urls:
To exclude certain URLs from being tracked, you can pass comma delimited regexes
to `instrument_app` as the keyword variable `excluded_urls`. For example:
```python
instrumentation.instrument_app(app, db.get_engine(), excluded_urls='.*static/,favicon.ico')
```


### Set up your own tags:
You can assign metadata to your resources in the form of tags.
Each tag is a label consisting of a user-defined key and value.
Tags can help you manage, identify, organize, search for, and filter resources.
You can create tags to categorize resources by purpose, owner, environment, or other criteria.

#### Define tags using environment variables:
METIS_TAG_<TAG_NAME>="<VALUE>"

```bash
export METIS_TAG_ENV=staging
export METIS_TAG_PR=$(git log -1 --format="%H")
```

#### Define tag using code:
Initialized setup with additional param called `resource_tags`

```python
from fastapialchemycollector import setup, MetisInstrumentor

instrumentation: MetisInstrumentor = setup('<service-name>',
                                           api_key="<api_key>"
                                           ...,
                                           resource_tags={"env": "staging"})
```