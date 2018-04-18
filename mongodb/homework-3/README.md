# COMS 3102 Homework 3

Wode "Nimo" Ni

- Assigned genre: Comedy
- Command used to import data:
```shell
mongorestore -d db -c movies ../movies.bson
```
- Note that my solution do require the database to be freshly imported. So please drop the database by running `use db` and then `db.dropDatabase()`. After that, run the script by `python homework-3.py`
- My output:
```shell
vagrant@ubuntu-xenial:/vagrant/homework-3$ mongorestore -d db -c movies ../movies.bson
2018-04-18T03:32:16.351+0000    checking for collection data in ../movies.bson
2018-04-18T03:32:16.370+0000    restoring db.movies from ../movies.bson
2018-04-18T03:32:19.348+0000    [########................]  db.movies  28.8MB/78.8MB  (36.6%)
2018-04-18T03:32:22.348+0000    [#################.......]  db.movies  58.2MB/78.8MB  (73.9%)
2018-04-18T03:32:24.872+0000    [########################]  db.movies  78.8MB/78.8MB  (100.0%)
2018-04-18T03:32:24.872+0000    no indexes to restore
2018-04-18T03:32:24.872+0000    finished restoring db.movies (46014 documents)
2018-04-18T03:32:24.872+0000    done
vagrant@ubuntu-xenial:/vagrant/homework-3$ python homework_3.py

Part A

Modified 0 documents

Part B

Inserted ID 5ad6bd2a962d745900ee85c7
{u'genres': [u'Comedy', u'Drama', u'Romance'], u'title': u'Love, Simon', u'countries': [u'USA'], u'directors': [u'Greg Berlanti'], u'imdb': {u'rating': 8.1, u'votes': 13767, u'id': 5164432}, u'year': 2018, u'_id': ObjectId('5ad6bd2a962d745900ee85c7')}

Part C

Counting the number of Comedy movies:
{u'count': 1, u'_id': u'Comedy'}

Part D

Counting the number of unrated Chinese movies:

Part E

{u'_id': ObjectId('5ad6bd2a962d745900ee85c8'),
 u'client': u'Bob',
 u'item': u'iPhone X',
 u'price': [999]}
{u'_id': ObjectId('5ad6bd2a962d745900ee85c9'),
 u'client': u'Alice',
 u'item': u'iPad Pro',
 u'price': [609]}
{u'_id': ObjectId('5ad6bd2a962d745900ee85ca'),
 u'client': u'Cody',
 u'item': u'Mac Pro',
 u'price': [1579]}
```

