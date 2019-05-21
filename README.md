BackpackTechnologies RESTful API with Flask & SQLAlchemy
===================
1. Install PostgreSQL (please definite "postgres" as password to the user "postgres" when the installer ask you for) : https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. Install PostgreSQL command line tools in case the previous installation isn't enough :
- for linux :
```shell
$ sudo apt-get install postgresql
```
- for mac :
```shell
$ brew install postgresql
```

3. Enable your virtual env

4. Install requisite packages:
```shell
$ pip install -r requirements.txt
```

5. Create and update local tables:
```shell
$ ./init_db.sh
```
- The first mdp is your root mdp
- The second is normaly "postgres" if you configure it right during installation

6. Run service:
```
$ python app.py
```

7. Give it a try:
```shell
>> import requests, json
>> requests.get('http://localhost:5000/users').json()
[]
>> requests.post('http://localhost:5000/users',
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({'username': 'username'})).json()
{u'id': 1, u'username': u'username', u'uri': u'http://localhost:5000/users/1'}
>> requests.get('http://localhost:5000/users/1').json()
{u'id': 1, u'username': u'username', u'uri': u'http://localhost:5000/users/1'}
>> requests.put('http://localhost:5000/users/1',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'username': 'username'})).json()
{u'id': 1, u'username': u'username', u'uri': u'http://localhost:5000/users/1'}
>> requests.delete('http://localhost:5000/users/1')
>> requests.get('http://localhost:5000/users').json()
[]
```

8. At each new release don't forget to run for upgrade the database
```shell
$ python manage.py db upgrade
```

Don't forget that you must pass a "Content-Type: application/json" header along with your request
