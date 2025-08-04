This repository contains a minimal FastAPI project. Your task is to extend the application by adding the features described below.

---

## 1. Quick-start

```bash
# Install the ASGI server
pip install uvicorn

# Install this project in editable mode (so code changes are picked up automatically)
pip install -e .

# Start the application with hot-reload enabled
uvicorn qhapp.main:app --reload
```

Unit tests can be run with:

```bash
pytest
```

## 2. Goals

### 2.1 Datasets endpoint

Create an endpoint that returns datasets.  

A returned dataset (JSON) object should have a structure that resembles the following:
```json
{
  "name": "my_dataset_name",
  "attributes": {
    "key1": ["value_1", "value_2"], 
    "key2": ["value_3"]
  },
  "files": [
    {
      "name": "test.py", 
      "status": "uploaded"
    }, 
    {
      "name": "test.hdf5", 
      "status": "in_progress"
    }
  ]
}
```

The client should be able to request the dataset either **with** or **without** the `files` field.

**Note**: Attribute key-value pairs are frequently shared across multiple datasets (e.g., the same `users` or `set_up` values appear in different datasets). Also consider that it should be possible to perform the filtering operations explained in the next section.

### 2.2 Attribute-filtering endpoint

This endpoint accepts attribute filters and returns all attribute key-value pairs that co-occur with the filtered datasets.

**How it works:**

1. *Input*: A set of attribute filters (e.g., `{"key_a": ["value1", "value7"], "key_b": ["value8"]}`)
2. *Process*: Find all datasets that match ALL specified filters:
   - Have `key_a` with value `"value1"` OR `"value7"` AND
   - Have `key_b` with value `"value8"`
3. *Output*: Return all attribute key-value pairs present in the matching datasets, excluding the filter attributes (e.g., if filtering by `users` and `project`, return all other attributes like `set_up`, `environment`, etc.)


Example datasets:

```json
// ds1
{
  "name": "ds1",
  "attributes": {
    "users": ["user_1", "user_2"],
    "set_up": ["XLD"],
    "project": ["2qubits"]
  },
  "files": []
}

// ds2
{
  "name": "ds2", 
  "attributes": {
    "users": ["user_3"],
    "set_up": ["XLD"],
    "project": ["qubit_read"]
  },
  "files": []
}

// ds3
{
  "name": "ds3",
  "attributes": {
    "users": ["user_2"],
    "set_up": ["VTT"]
  },
  "files": []
}
```

If the client supplies the filter `users=["user_2"]`, the server should return every key–value pair present in the selected datasets:

```json
{
  "set_up": ["XLD", "VTT"],
  "project": ["2qubits"]
}
```

Multiple filters can be combined.  
For instance, `users=["user_1","user_2"]` and `project=["2qubits"]` should:
1. Find datasets matching BOTH filters (only **ds1** matches)
2. Return all other attributes from **ds1** (excluding the filter attributes):

```json
{
  "set_up": ["XLD"]
}
```

---

## 3. Bonus

* Add unit tests
* Implement error handling
