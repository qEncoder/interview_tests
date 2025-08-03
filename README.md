This repository contains an empty project (fastapi) of a webapp where the goal is to extend the application.

---

## 1. Quick-start

```bash
pip3 install uvicorn
pip3 install -e .

uvicorn qhapp.main:app --reload
```

## goals:

1) add an endpoint that implements getting datasets, a dataset contains several fields:
	* name
	* attributes e.g. {'users' : ["user_1", "user_2"] , "set_up" = ["set_up_1"], ... }
	* files (e.g. [file_1, file_2]). The file has a name, and storage location.

Is should be possible to retrieve the dataset object, along with/witout the files.

2) add an enpoint that allows you te retrieve attributes, based on a set of given attibutes, example:

Say there are three datasets with the following attibutes

ds1 :

| attr key | attr value |
-------------------------
| users    | user_1     |
| users    | user_2     |
| set_up   | XLD        |
| project  | 2qubits    |

ds2 :

| attr key | attr value |
-------------------------
| users    | user_3     |
| set_up   | XLD        |
| project  | qubit_read |


ds2 :

| attr key | attr value |
-------------------------
| users    | user_2     |
| set_up   | VTT        |

In this example:

When the users : user_2 is provided, the server should return all attributes that occur in common:

So in this example that would return:

| attr key | attr value |
-------------------------
| set_up   | XLD        |
| set_up   | VTT        |
| project  | 2qubits    |

It should also be possible to make multiple selections, e.g. users : user_1 and user_2 + project : 2qubits

In this case it returns

| attr key | attr value |
-------------------------
| project  | 2qubits    |

Bonusses ::
** add unit testing
** extensive error handling
