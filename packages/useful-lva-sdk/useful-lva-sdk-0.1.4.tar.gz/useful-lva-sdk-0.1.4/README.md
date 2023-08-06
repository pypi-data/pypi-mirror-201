# Vertex AI Vision Live Video Analytics SDK 
*Unofficial Vertex AI Vision SDK in Python.* It's for building Live Video Analytics (LVA) program and CRUD LVA resources. 

## Installation

```commandline
pip install useful-lva-sdk
```

## Get started

Create an LVA program with this lib:

```python
from src.useful_lva_sdk.core import LvaGraphBuilder
from src.useful_lva_sdk.core.operator import *

graph = LvaGraphBuilder("test-analysis")
    .add_analyzer(GcsVideoSource(), "gcs_source")
    .add_analyzer(GcsProtoSink(), "gcs_sink")
    .add_analyzer(OccupancyCounting(), "oc")
    .connect("oc", "gcs_sink")
    .connect("gcs_source", "oc")
    .build()
```

Create an analysis with this lib:

```python
from src.useful_lva_sdk.client.lva_client import LVAClient

analysis = graph.analysis()
client = LVAClient(
    project="PROJECT_ID",
    location="LOCATION_ID",
    cluster="CLUSTER_ID",
)
client.create_analysis(analysis.name, analysis)
```