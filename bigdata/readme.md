# Big Data: Complete Notes

This document provides concise, production‑oriented notes on Big Data fundamentals, distributed processing, cluster architecture, and the broader ecosystem.

---

## 1) Big Data

### Definition (4+1 V’s)
- Volume: TB→PB scale data that exceeds single‑machine capacity.
- Velocity: Rapid ingestion (batch and real‑time streams).
- Variety: Structured (tables), semi‑structured (JSON/Parquet), unstructured (text, images, audio, video).
- Veracity: Data quality, noise, missingness, bias.
- Value: Business outcomes extracted from the data.

### Data Types
- Structured: Fixed schema, e.g., RDBMS tables.
- Semi‑structured: JSON, Avro, Parquet with schema‑on‑read.
- Unstructured: Free text, media; requires extraction or embeddings.

### Traditional Systems vs. Big‑Data Needs
- Scale‑up vs. Scale‑out: Bigger single server vs. many commodity nodes.
- Storage: Local disk vs. distributed file systems with replication.
- Processing: Single‑threaded ETL vs. parallel execution engines.
- Consistency: Strong ACID vs. eventual consistency and partition tolerance where appropriate.
- Workloads: Short OLTP vs. long‑running analytical/ML pipelines.

### Real‑World Applications
- Clickstream analytics and growth funnels
- Fraud detection and risk scoring
- Observability/log analytics and security
- Recommendation systems, feature stores, and model training

---

## 2) Distributed Processing Frameworks

### Why Distributed?
- Data exceeds one machine’s storage/CPU/memory.
- Parallelism reduces wall‑clock time; tasks run across nodes.
- Data locality minimizes network I/O by moving compute to the data.
- Fault tolerance: failed tasks are retried on other nodes.

### Hadoop: HDFS + MapReduce
- HDFS: Distributed, fault‑tolerant storage; large block sizes (e.g., 128MB), replication (e.g., 3).
- MapReduce: Map → Shuffle/Sort → Reduce; highly reliable for batch; disk‑heavy between stages.

### Limits of MapReduce vs. Spark Advantages
- MapReduce:
  - Writes to disk after each stage; poor for iterative algorithms and interactive queries.
  - Job chaining is cumbersome.
- Apache Spark:
  - In‑memory processing (RDD/DataFrame), DAG scheduler, lazy evaluation.
  - Unified APIs: SQL, batch, streaming, ML.
  - Catalyst optimizer and Tungsten engine for vectorized execution.

---

## 3) Distributed Architecture

### Cluster Roles
- Master/Control Plane:
  - HDFS NameNode (+ Standby) and JournalNodes for metadata durability.
  - YARN ResourceManager (+ Standby) for cluster scheduling.
- Workers:
  - HDFS DataNode stores blocks and serves reads/writes.
  - YARN NodeManager runs containers; Spark executors live here.

### Core Daemons
- HDFS:
  - NameNode: Namespace and block location metadata.
  - DataNode: Stores/serves blocks; sends heartbeats and block reports.
  - HA: Active/Standby NN with shared edit logs (JournalNodes).
- YARN:
  - ResourceManager: Allocates resources across applications.
  - NodeManager: Manages containers/resources per node.
  - ApplicationMaster: Per‑application orchestrator (e.g., Spark driver).

### Heartbeats & Fault Tolerance
- Heartbeats: DataNodes and NodeManagers send periodic signals; absence ⇒ failure handling.
- Replication: Blocks replicated across nodes; re‑replication on failures.
- Speculative execution: Launch duplicate attempts for slow tasks to reduce tail latency.
- Lineage/Checkpointing: Spark recomputes lost partitions; shuffle persistence improves robustness.

---

## 4) Ecosystem Overview

- Hive: SQL on data lakes; Metastore provides table metadata; often queried by Spark/Trino.
- Kafka: Distributed commit log for high‑throughput event streaming and decoupled producers/consumers.
- Flume/Logstash/Kafka Connect: Ingestion from logs and databases; Debezium for CDC.
- Sqoop: Legacy bulk RDBMS↔HDFS transfer (often replaced by Spark connectors).
- HBase: Wide‑column NoSQL on HDFS for low‑latency random reads/writes.
- Trino/Presto: MPP SQL engine over multiple sources (object stores, RDBMS, NoSQL).
- Spark Structured Streaming / Flink: Exactly‑once, stateful stream processing.
- Airflow/Oozie: Workflow orchestration and scheduling.
- Zookeeper: Coordination service used by Kafka, HBase, and Hadoop HA.

---

## Practical Guidance
- File formats: Prefer columnar (Parquet/ORC) with compression for analytics.
- Partitioning & pruning: Partition by time (dt=YYYY‑MM‑DD) or business keys; avoid over‑partitioning.
- Small files problem: Batch or compact outputs to avoid millions of tiny files.
- Skew & joins: Use salting/repartitioning; broadcast small dimension tables in Spark SQL.
- Governance: Centralize schemas (Hive/Glue), enforce access controls, and audit usage.

---

## Quick Commands
```bash
# HDFS
hdfs dfs -mkdir -p /data/events
hdfs dfs -put local.parquet /data/events/
hdfs dfs -ls /data/events

# Spark (local)
spark-shell
# Example:
# val df = spark.read.parquet("/data/events")
# df.groupBy($"dt").count.show()
```
