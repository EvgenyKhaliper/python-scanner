# Scanning engine in Python
## Prerequisites
1. run _./devops.sh_ build to build docker images
2. run _./devops.sh_ refresh to create/refresh postgres/redis/rabbitmq containers
3. make sure to add POSTGRES_CONNECTION, RABBIT_HOST and REDIS_HOST environment variables to each project, otherwise mock will be in place
    * _POSTGRES_CONNECTION=host='localhost' dbname='testdb' user='admin' password='admin'_
    * _RABBIT_HOST=localhost_
    * _REDIS_HOST=host=localhost_
4. pip install requirements.txt
## Structure
1. **api** - _flask endpoint, api gateway_
2. **scan_processor** - _flask endpoint, sends scans to execution and updates cache_
3. **scan_executer** - _flask endpoint, executes 2 scans concurrently_
4. **shared** - _package with persistence clients and shared objects_