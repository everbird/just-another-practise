# Just Another Homework to practise
## Problem Description
```
Create service that merges data from 2 cross-referenced MongoDB collections into the third one.

collection1
{
  _id:
  collection2_id:
  data: value
}
collection2
{
  _id:
  collection1_id:
  data:
}
collection3
{
  _id:
  item1: {
    _id:
    collection2_id:
    data: value
  }
  item2: {
    _id:
    collection1_id:
    data:
  }
}

Requirements:
- Documents are exported only if the following property is specified
{
  ...
  completed: true
}
- It should be possible to run multiple instances of the service concurrently with work being evenly distributed
across those instances. Each document marked as “completed” should still be exported exactly once.
```

## My Solution
Actually it would be better if there are some test data for collection1 and collection2. I assume that there are some documents with `completed: true` property randomly, only in collection1 and collection2. It is easy to find out the cross-referenced pairs. Just use a worker to scan from last ObjectId and put the pairs it found into a queue. Multiple consumer workers will BRPOP them taking the advantage of Redis and merge them into collection3 concurrently. Export documents process is almost the same. A worker scan for documents with `completed: true` property. Put them in a queue. BRPOP them and mongoexport them to file system.

## How to Setup the Demo
This demo dependent on mongodb, redis. Pls make sure if them have been installed.

1. git clone https://github.com/everbird/just-another-practise.git homework
2. cd homework. Active the virtualenv is you like.
3. make build_env req ss
4. make st. All the apps should be RUNNING
5. make init_data. Generate some test data in mongodb.
6. Check out the ./log/celery.log or celery flower at http://localhost:8114. You can see what is going on.
7. Check out the ./data/export. `completed` documents will be exported here.
