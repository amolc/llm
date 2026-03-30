# Introduction to Apache Spark

This note gives a concise, practical introduction to Apache Spark, its ecosystem, where it fits vs. Hadoop, and how it runs on cluster managers like YARN alongside HDFS.

---

## What is Apache Spark?
- A distributed compute engine for large‑scale data processing with in‑memory execution and a DAG scheduler.
- Provides high‑level APIs in Python (PySpark), Scala, SQL, R, and Java.
- Unifies multiple workloads in a single framework: batch, SQL, streaming, ML, and graph analytics.

Key ideas:
- Resilient Distributed Datasets (RDDs) and higher‑level DataFrames/Datasets.
- Lazy evaluation with an optimizer (Catalyst) and efficient execution (Tungsten).
- Fault tolerance via lineage: lost partitions can be recomputed.

---

## Spark Ecosystem Overview
- Core APIs: RDD, DataFrame, Dataset.
- Spark SQL: ANSI SQL over structured data; integrates with Hive Metastore.
- Structured Streaming: Micro‑batch/continuous processing with exactly‑once semantics.
- MLlib: Feature engineering, classical ML algorithms, pipelines.
- GraphX (Scala): Graph processing on RDDs.
- Connectors: Parquet/ORC, CSV/JSON, JDBC, Delta/iceberg/hudi, Kafka, Cassandra, Elastic, more.

---

## Spark vs. Hadoop (MapReduce)
- Execution model:
  - MapReduce: map → shuffle → reduce; writes to disk between stages.
  - Spark: DAG of stages and in‑memory caching; faster for iterative and interactive jobs.
- APIs:
  - MapReduce: low‑level Java; complex to chain jobs.
  - Spark: high‑level DataFrame/SQL and rich libraries (Streaming, MLlib).
- Use cases:
  - MapReduce: robust batch ETL historically.
  - Spark: unified analytics (ETL + SQL + streaming + ML) with lower latency.

Note: Hadoop is an ecosystem. Spark often runs on top of Hadoop storage (HDFS) and resource managers (YARN), complementing rather than “replacing” it.

---

## Spark Architecture and Components
- Driver: Orchestrates the application; builds the logical plan/DAG; coordinates tasks.
- Cluster Manager: Allocates resources (Standalone, YARN, Kubernetes).
- Executors: Run tasks on worker nodes; hold cached data.
- DAG Scheduler: Splits the job into stages separated by shuffles; tasks are parallel units.
- Catalyst Optimizer (SQL/DataFrame): Logical plan → optimized plan → physical plan.
- Tungsten: Code generation and memory management for efficient execution.

Execution flow:
1. User code builds a DataFrame/SQL query (lazy).
2. Catalyst optimizes; DAG scheduler plans stages.
3. Tasks are sent to executors; shuffle exchanges connect stages.
4. Results returned to the driver or written to storage.

---

## Spark in the Hadoop Ecosystem (YARN, HDFS)
- Storage: Read/write from HDFS using Parquet/ORC for columnar performance.
- Resource Management: Submit Spark applications to YARN (cluster or client mode), or run on Standalone/Kubernetes.
- Metastore: Use Hive Metastore for table/partition metadata; Spark SQL can query Hive tables.
- Security/Policies: Leverage Hadoop auth (Kerberos), Ranger/Atlas, and HDFS ACLs where applicable.

---

## Quick Start Snippets

PySpark (local):
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("quickstart").getOrCreate()
df = spark.read.csv("data/events.csv", header=True, inferSchema=True)
df.groupBy("event_date").count().orderBy("event_date").show()
spark.stop()
```

Spark SQL (shell):
```bash
spark-sql -e "SELECT date, COUNT(*) FROM parquet.'hdfs:///data/logs' GROUP BY date ORDER BY date"
```

Submit to YARN (example):
```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --class org.example.Job \
  your-assembly-or-wheel-here
```

---

## Recommended Videos & Playlists
- Databricks YouTube channel (Data + AI Summit sessions, Spark fundamentals): https://www.youtube.com/@databricks
- The Apache Software Foundation channel (project talks, community content): https://www.youtube.com/@TheApacheFoundation
- Search on YouTube:
  - “Matei Zaharia Introduction to Apache Spark”
  - “Spark SQL and Catalyst Optimizer talk”
  - “Structured Streaming fundamentals Databricks”

These sources provide high‑quality introductions, deep dives into Spark SQL/Structured Streaming, and real‑world performance tuning sessions.
