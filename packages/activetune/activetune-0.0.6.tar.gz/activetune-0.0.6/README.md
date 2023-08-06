# Activetune Python SDK


## Install

```sh
pip install activetune
```


## Usage

Create API instance sing user token copied for Activetune dashboard:

```python
import activetune as at

api = at.Api(token="<your Activetune token here>")
```

Alternatively, you can pass user token via environment variable `ACTIVETUNE_TOKEN`

```python

# export ACTIVETUNE_TOKEN = ...

api = at.Api()

```


### Create dataset

```python
ds_id = api.create_dataset(name="MyDataset", description="this is my dataset")
```

### List datasets

```python
api.list_datasets()
```


### Get all data in a dataset

```python
api.get_data(dataset_id=ds_id)
```

### Add data to a dataset

```python
sample_id = api.add_sample(dataset_id=ds_id, input="hi", model_output="hello", model_id="my_model_id")
```

### Send feedback for a sample

```python
api.set_feedback(sample_id=sample_id, feedback=5)   # 0 <= feedback <= 5
```


