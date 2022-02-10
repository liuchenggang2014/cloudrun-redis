# cloudrun-redis

## pre-requirement
1. create a memorystore-redis in private service access mode to better use the vpc ip range
[create redis with psa connection](https://cloud.google.com/memorystore/docs/redis/establishing-connection)
2. create cloud sql instance with private ip
3. install mongo community eddtion in local gce
4. create a serverless vpc access
[create serverless vpc access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access#restrict-access)

## deploy cloud run with envirnment variables
1. change the cloud build var with your project and networking information
2. gcloud builds submit 
