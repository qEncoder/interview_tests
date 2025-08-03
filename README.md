This repository contains a minimal FastAPI project. Your task is to extend the application by adding the features described below.

---

## 1. Quick-start

```bash
pip install uvicorn
pip install -e .

uvicorn qhapp.main:app --reload
```


## 2. Goals

### 2.1 Datasets endpoint

Create an endpoint that returns datasets.  
Each dataset must contain:

* `name`
* `attributes` – which can map, for example  
  `{"users": ["user_1", "user_2"], "set_up": ["set_up_1"], ...}`
* `files` – a list of files, each with a `name` and a `storage_location`

The client should be able to request the dataset either **with** or **without** the `files` field.

### 2.2 Attribute-filtering endpoint

Implement an endpoint that, given a set of attribute filters, returns all matching attribute key–value pairs across datasets.

Example datasets:

**ds1**

| Key | Value |
| --- | ----- |
| users | user_1 |
| users | user_2 |
| set_up | XLD |
| project | 2qubits |

**ds2**

| Key | Value |
| --- | ----- |
| users | user_3 |
| set_up | XLD |
| project | qubit_read |

**ds3**

| Key | Value |
| --- | ----- |
| users | user_2 |
| set_up | VTT |

If the client supplies the filter `users=[user_2]`, the server should return every key–value pair present in the selected datasets:

| Key | Value |
| --- | ----- |
| set_up | XLD |
| set_up | VTT |
| project | 2qubits |

Multiple filters can be combined.  
For instance, `users=[user_1,user_2]`, and `project=[2qubits]` should yield (only one option in this example):

| Key | Value |
| --- | ----- |
| project | 2qubits |

---

## 3. Bonus

* Add unit tests
* Implement error handling