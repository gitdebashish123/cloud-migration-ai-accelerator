# cloud-migration-ai-accelerator

This is a POC project to develop generic AI accelerators for different migration use cases

## Project set up

include all relevant libraries to requirements.txt and run below command

```bash
pip install -r requirements.txt
```

## Useful Commands

```bash

# create python env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# generate llm template
python3 src/prompts/prompt_generator/gen_hive_to_iceberg_conversion_template.py

# run streamlit app
streamlit run src/cloud_ai_accelerator_tool.py 


# set OpenAI key under .env file present under root dir as and 
# include .env as part of .gitignore
OPENAI_API_KEY = "sk-proj-Cwb6MvaD4YA****"

```

## Hadoop Commands

```bash

# Daemons start
hdfs namenode -format
start-dfs.sh
start-yarn.sh
# Check services
jps

NameNode
DataNode
ResourceManager
NodeManager
SecondaryNameNode


# Daemons stop
stop-dfs.sh
stop-yarn.sh

# Hive Services
hive --service metastore &
hive --service hiveserver2 &
```
## Hive Sample Data
~~~~sql
update employee
  set salary = salary * 2
  where salary < 100000
~~~~

## Hadoop UI

 - [NameNode](http://localhost:9870)
 - [SecondaryNameNode](http://localhost:9868)
 - [ResourceManager](http://localhost:8088)
