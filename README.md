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

