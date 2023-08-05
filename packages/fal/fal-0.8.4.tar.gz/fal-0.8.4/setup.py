# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'tests'}

packages = \
['_fal_testing',
 'fal',
 'fal.cli',
 'fal.cli.model_generator',
 'fal.feature_store',
 'fal.packages',
 'fal.packages.environments',
 'fal.planner',
 'fal.telemetry',
 'faldbt',
 'faldbt.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'agate-sql>=0.5.8,<0.6.0',
 'astor>=0.8.1,<0.9.0',
 'backports.functools_lru_cache>=1.6.4,<2.0.0',
 'dbt-core>=1.4,<1.5',
 'deprecation>=2.1.0,<3.0.0',
 'dill>=0.3.5.1,<0.3.6',
 'importlib-metadata>=4.12.0',
 'packaging<22',
 'pandas>=1.3.4,<2.0.0',
 'platformdirs>=2.5.2,<3.0.0',
 'posthog>=1.4.5,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'virtualenv>=20.16.2,<21.0.0']

extras_require = \
{'bigquery': ['google-cloud-bigquery[pandas]>=3.5.0,<3.6.0'],
 'cloud': ['koldstart>=0.6.16,<0.7.0'],
 'dev': ['matplotlib>=3.5.2,<4.0.0'],
 'duckdb': ['duckdb-engine>=0.1.8,<0.2.0'],
 'redshift': ['sqlalchemy-redshift>=0.8.9,<0.9.0'],
 'snowflake': ['snowflake-connector-python[pandas]>=2.8.0,<2.8.2'],
 'test': ['pytest>=5.2,<6.0',
          'black>=22.3,<23.0',
          'behave>=1.2.6,<2.0.0',
          'mock>=4.0.3,<5.0.0',
          'pytest-mock>=3.7.0,<4.0.0']}

entry_points = \
{'console_scripts': ['fal = fal.cli:cli']}

setup_kwargs = {
    'name': 'fal',
    'version': '0.8.4',
    'description': 'fal allows you to run python scripts directly from your dbt project.',
    'long_description': '<!-- <base href="https://github.com/fal-ai/fal/blob/-/projects/fal/" target="_blank" /> -->\n\n# fal: do more with dbt\n\nfal is the easiest way to run Python with your [dbt](https://www.getdbt.com/) project.\n\n# Introduction\n\nWith the `fal` CLI, you can:\n\n- [Send Slack notifications](https://github.com/fal-ai/fal/blob/-/examples/slack-example) upon dbt model success or failure.\n- [Load data from external data sources](https://blog.fal.ai/populate-dbt-models-with-csv-data/) before a model starts running.\n- [Download dbt models](https://docs.fal.ai/fal/python-package) into a Python context with a familiar syntax: `ref(\'my_dbt_model\')` using `FalDbt`\n- [Programatically access rich metadata](https://docs.fal.ai/fal/reference/variables-and-functions) about your dbt project.\n\nHead to our [documentation site](https://docs.fal.ai/) for a deeper dive or play with [in-depth examples](https://github.com/fal-ai/fal/blob/-/examples/README.md) to see how fal can help you get more done with dbt.\n\n> ❗️ If you would like to write data back to your data-warehouse, we recommend using the [`dbt-fal`](https://pypi.org/project/dbt-fal/) adapter.\n\n# Getting Started\n\n## 1. Install `fal`\n\n```bash\n$ pip install fal\n```\n\n## 2. Go to your dbt project directory\n\n```bash\n$ cd ~/src/my_dbt_project\n```\n\n## 3. Create a Python script: `send_slack_message.py`\n\n```python\nimport os\nfrom slack_sdk import WebClient\nfrom slack_sdk.errors import SlackApiError\n\nCHANNEL_ID = os.getenv("SLACK_BOT_CHANNEL")\nSLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")\n\nclient = WebClient(token=SLACK_TOKEN)\nmessage_text = f"Model: {context.current_model.name}. Status: {context.current_model.status}."\n\ntry:\n    response = client.chat_postMessage(\n        channel=CHANNEL_ID,\n        text=message_text\n    )\nexcept SlackApiError as e:\n    assert e.response["error"]\n```\n\n## 4. Add a `meta` section in your `schema.yml`\n\n```yaml\nmodels:\n  - name: historical_ozone_levels\n    description: Ozone levels\n    config:\n      materialized: table\n    columns:\n      - name: ozone_level\n        description: Ozone level\n      - name: ds\n        description: Date\n    meta:\n      fal:\n        scripts:\n          - send_slack_message.py\n```\n\n## 5. Run `fal flow run`\n\n```bash\n$ fal flow run\n# both your dbt models and fal scripts are run\n```\n\n## 6. Alternatively run `dbt` and `fal` consecutively\n\n```bash\n$ dbt run\n# Your dbt models are run\n\n$ fal run\n# Your python scripts are run\n```\n\n# Examples\n\nTo explore what is possible with fal, take a look at the in-depth examples below. We will be adding more examples here over time:\n\n- [Example 1: Send Slack notifications](https://github.com/fal-ai/fal/blob/-/examples/slack-example/README.md)\n- [Example 2: Use dbt from a Jupyter Notebook](https://github.com/fal-ai/fal/blob/-/examples/write_jupyter_notebook/README.md)\n- [Example 3: Read and parse dbt metadata](https://github.com/fal-ai/fal/blob/-/examples/read_dbt_metadata/README.md)\n- [Example 4: Metric forecasting](https://github.com/fal-ai/fal/blob/-/examples/metric-forecast/README.md)\n- [Example 5: Sentiment analysis on support tickets](https://github.com/fal-ai/fal/blob/-/examples/sentiment-analysis/README.md)\n- [Example 6: Anomaly Detection](https://github.com/fal-ai/fal/blob/-/examples/anomaly-detection/README.md)\n- [Example 7: Incorporate fal in CI/CD workflow](https://github.com/fal-ai/fal/blob/-/examples/ci_example/README.md)\n- [Example 8: Send events to Datadog](https://github.com/fal-ai/fal/blob/-/examples/datadog_event/README.md)\n- [Example 9: Write dbt artifacts to GCS](https://github.com/fal-ai/fal/blob/-/examples/write_to_gcs/README.md)\n- [Example 10: Write dbt artifacts to AWS S3](https://github.com/fal-ai/fal/blob/-/examples/write_to_aws/README.md)\n\n[Check out the examples directory for more](https://github.com/fal-ai/fal/blob/-/examples/README.md)\n\n# How it works?\n\n`fal` is a command line tool that can read the state of your `dbt` project and help you run Python scripts after your `dbt run`s by leveraging the [`meta` config](https://docs.getdbt.com/reference/resource-configs/meta).\n\n```yaml\nmodels:\n  - name: historical_ozone_levels\n    ...\n    meta:\n      fal:\n        post-hook:\n          # scripts will run concurrently\n          - send_slack_message.py\n          - another_python_script.py\n```\n\n`fal` also provides useful helpers within the Python context to seamlessly interact with dbt models: `ref("my_dbt_model_name")` will pull a dbt model into your Python script as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).\n\n## Running scripts before dbt runs\n\nRun scripts before the model runs by using the `pre-hook:` configuration option.\n\nGiven the following schema.yml:\n\n```\nmodels:\n  - name: boston\n    description: Ozone levels\n    config:\n      materialized: table\n    meta:\n      owner: "@meder"\n      fal:\n        pre-hook:\n          - fal_scripts/trigger_fivetran.py\n        post-hook:\n          - fal_scripts/slack.py\n```\n\n`fal flow run` will run `fal_scripts/trigger_fivetran.py`, then the `boston` dbt model, and finally `fal_scripts/slack.py`.\nIf a model is selected with a selection flag (e.g. `--select boston`), the hooks associated to the model will always run with it.\n\n```bash\n$ fal flow run --select boston\n```\n\n# Concepts\n\n## profile.yml and Credentials\n\n`fal` integrates with `dbt`\'s `profile.yml` file to access and read data from the data warehouse. Once you setup credentials in your `profile.yml` file for your existing `dbt` workflows anytime you use `ref` or `source` to create a dataframe `fal` authenticates using the credentials specified in the `profile.yml` file.\n\n## `meta` Syntax\n\n```yaml\nmodels:\n  - name: historical_ozone_levels\n    ...\n    meta:\n      owner: "@me"\n      fal:\n        post-hook:\n          - send_slack_message.py\n          - another_python_script.py\n```\n\nUse the `fal` and `post-hook` keys underneath the `meta` config to let `fal` CLI know where to look for the Python scripts. You can pass a list of scripts as shown above to run one or more scripts as a post-hook operation after a `dbt run`.\n\n## Variables and functions\n\nInside a Python script, you get access to some useful variables and functions\n\n### Variables\n\nA `context` object with information relevant to the model through which the script was run. For the [`meta` Syntax](#meta-syntax) example, we would get the following:\n\n```python\ncontext.current_model.name\n#= historical_ozone_levels\n\ncontext.current_model.meta\n#= {\'owner\': \'@me\'}\n\ncontext.current_model.meta.get("owner")\n#= \'@me\'\n\ncontext.current_model.status\n# Could be one of\n#= \'success\'\n#= \'error\'\n#= \'skipped\'\n```\n\n`context` object also has access to test information related to the current model. If the previous dbt command was either `test` or `build`, the `context.current_model.test` property is populated with a list of tests:\n\n```python\ncontext.current_model.tests\n#= [CurrentTest(name=\'not_null\', modelname=\'historical_ozone_levels, column=\'ds\', status=\'Pass\')]\n```\n\n### `ref` and `source` functions\n\nThere are also available some familiar functions from `dbt`\n\n```python\n# Refer to dbt models or sources by name and returns it as `pandas.DataFrame`\nref(\'model_name\')\nsource(\'source_name\', \'table_name\')\n\n# You can use it to get the running model data\nref(context.current_model.name)\n```\n\n### `write_to_model` function\n\n> ❗️ We recommend using the [`dbt-fal`](https://pypi.org/project/dbt-fal/) adapter for writing data back to your data-warehouse.\n\nIt is also possible to send data back to your data-warehouse. This makes it easy to get the data, process it and upload it back into dbt territory.\n\nThis function is available in fal Python models only, that is a Python script inside a `fal_models` directory and add a `fal-models-paths` to your `dbt_project.yml`\n\n```yaml\nname: "jaffle_shop"\n# ...\nmodel-paths: ["models"]\n# ...\n\nvars:\n  # Add this to your dbt_project.yml\n  fal-models-paths: ["fal_models"]\n```\n\nOnce added, it will automatically be run by fal without having to add any extra configurations in the `schema.yml`.\n\n```python\nsource_df = source(\'source_name\', \'table_name\')\nref_df = ref(\'a_model\')\n\n# Your code here\ndf = ...\n\n# Upload a `pandas.DataFrame` back to the datawarehouse\nwrite_to_model(df)\n```\n\n`write_to_model` also accepts an optional `dtype` argument, which lets you specify datatypes of columns. It works the same way as `dtype` argument for [`DataFrame.to_sql` function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html).\n\n```python\nfrom sqlalchemy.types import Integer\n# Upload but specifically create the `value` column with type `integer`\n# Can be useful if data has `None` values\nwrite_to_model(df, dtype={\'value\': Integer()})\n```\n\n## Importing `fal` as a Python package\n\nYou may be interested in accessing dbt models and sources easily from a Jupyter Notebook or another Python script.\nFor that, just import the `fal` package and intantiate a FalDbt project:\n\n```py\nfrom fal import FalDbt\nfaldbt = FalDbt(profiles_dir="~/.dbt", project_dir="../my_project")\n\nfaldbt.list_sources()\n# [\n#    DbtSource(name=\'results\' ...),\n#    DbtSource(name=\'ticket_data_sentiment_analysis\' ...)\n#    ...\n# ]\n\nfaldbt.list_models()\n# [\n#    DbtModel(name=\'zendesk_ticket_data\' ...),\n#    DbtModel(name=\'agent_wait_time\' ...)\n#    ...\n# ]\n\n\nsentiments = faldbt.source(\'results\', \'ticket_data_sentiment_analysis\')\n# pandas.DataFrame\ntickets = faldbt.ref(\'stg_zendesk_ticket_data\')\n# pandas.DataFrame\n```\n\n# Supported `dbt` versions\n\nThe latest `fal` version currently supports dbt `1.4.*`.\n\nIf you need another version, [open an issue](https://github.com/fal-ai/fal/issues/new) and we will take a look!\n\n# Contributing / Development\n\nWe use Poetry for dependency management and easy development testing.\n\nUse Poetry shell to trying your changes right away:\n\n```sh\n~ $ cd fal\n\n~/fal $ poetry install\n\n~/fal $ poetry shell\nSpawning shell within [...]/fal-eFX98vrn-py3.8\n\n~/fal fal-eFX98vrn-py3.8 $ cd ../dbt_project\n\n~/dbt_project fal-eFX98vrn-py3.8 $ fal flow run\n19:27:30  Found 5 models, 0 tests, 0 snapshots, 0 analyses, 165 macros, 0 operations, 0 seed files, 1 source, 0 exposures, 0 metrics\n19:27:30 | Starting fal run for following models and scripts:\n[...]\n```\n\n## Running tests\n\nTests rely on a Postgres database to be present, this can be achieved with docker-compose:\n\n```sh\n~/fal $ docker-compose -f tests/docker-compose.yml up -d\nCreating network "tests_default" with the default driver\nCreating fal_db ... done\n\n# Necessary for the import test\n~/fal $ dbt run --profiles-dir tests/mock/mockProfile --project-dir tests/mock\nRunning with dbt=1.0.1\n[...]\nCompleted successfully\nDone. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5\n\n~/fal $ pytest -s\n```\n\n# Why are we building this?\n\nWe think `dbt` is great because it empowers data people to get more done with the tools that they are already familiar with.\n\n`dbt`\'s SQL only design is powerful, but if you ever want to get out of SQL-land and connect to external services or get into Python-land for any reason, you will have a hard time. We built `fal` to enable Python workloads (sending alerts to Slack, building predictive models, pushing data to non-data-warehouse destinations and more) **right within `dbt`**.\n\nThis library will form the basis of our attempt to more comprehensively enable **data science workloads** downstream of `dbt`. And because having reliable data pipelines is the most important ingredient in building predictive analytics, we are building a library that integrates well with dbt.\n\n# Have feedback or need help?\n\n- Join us in [fal on Discord](https://discord.com/invite/Fyc9PwrccF)\n- Join the [dbt Community](http://community.getdbt.com/) and go into our [#tools-fal channel](https://getdbt.slack.com/archives/C02V8QW3Q4Q)\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fal-ai/fal/blob/-/projects/fal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
