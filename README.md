
# Leager

simple passbook startement with feacher like expoet csv file 


## API Reference

#### Get all items

```http
  GET /api/user/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `DATE` | `datetime` |  create date |
| `PARTICULARS` | `string` | reason |
| `DEBIT` | `int` | debit |
| `CREDIT` | `int` | credit |
| `BALANCE` | `int` | balance |

#### Get item

```http
  GET /api/usercreate/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Debit`      | `int` | debit |
| `Credit`      | `int` | credit |
| `Particular`      | `string` | reason |


#### Get item

```http
  GET /api/export/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `startdate`      | `date` | date |
| `enddate`      | `date` | date |
| `Particular`      | `string` | reason |



## Usage/Examples
Activate venv
```python3
source Downloads/banking/venv/bin/activate
```
makemigrations
```python3
python3 manage.py makemigrations

```
migrate
```python3
python3 manage.py migrate
```
populate database
```python3
python3 populate.py 
```
server start
```python3
python3 manage.py runserver
```
local host

```bash
http://127.0.0.1:8000/api/user/
```
