# COMS 3102 Homework 3

Wode "Nimo" Ni <br>
UNI: wn2155

- Assigned genre: Comedy
- Command used to import data:
```shell
mongorestore -d db -c movies ../movies.bson
```
- Note that my solution do require the database to be freshly imported. So please drop the database by running `use db` and then `db.dropDatabase()`. After that, use the above command to import data into the database and run the script by `python homework-3.py`
    - if you can, install `pprint` by `pip install pprint`. Things look a lot better that way!
- My output:
```shell
vagrant@ubuntu-xenial:/vagrant/homework-3$ mongorestore -d db -c movies ../movies.bson
2018-04-18T03:41:26.365+0000    checking for collection data in ../movies.bson
2018-04-18T03:41:26.399+0000    restoring db.movies from ../movies.bson
2018-04-18T03:41:29.355+0000    [#######.................]  db.movies  23.9MB/78.8MB  (30.3%)
2018-04-18T03:41:32.355+0000    [################........]  db.movies  54.9MB/78.8MB  (69.6%)
2018-04-18T03:41:34.951+0000    [########################]  db.movies  78.8MB/78.8MB  (100.0%)
2018-04-18T03:41:34.951+0000    no indexes to restore
2018-04-18T03:41:34.951+0000    finished restoring db.movies (46014 documents)
2018-04-18T03:41:34.951+0000    done
vagrant@ubuntu-xenial:/vagrant/homework-3$ python homework_3.py

Part A

Modified 508 documents

Part B

Inserted ID 5ad6be71962d7459474c2561
{u'genres': [u'Comedy', u'Drama', u'Romance'], u'title': u'Love, Simon', u'countries': [u'USA'], u'directors': [u'Greg Berlanti'], u'imdb': {u'rating': 8.1, u'votes': 13767, u'id': 5164432}, u'year': 2018, u'_id': ObjectId('5ad6be71962d7459474c2561')}

Part C

Counting the number of Comedy movies:
{u'count': 14046, u'_id': u'Comedy'}

Part D

Counting the number of unrated Chinese movies:
{u'count': 6, u'_id': {u'rated': u'Pending rating', u'countries': u'China'}}

Part E

{u'_id': ObjectId('5ad6be71962d7459474c2562'),
 u'client': u'Bob',
 u'item': u'iPhone X',
 u'price': 999}
{u'_id': ObjectId('5ad6be71962d7459474c2563'),
 u'client': u'Alice',
 u'item': u'iPad Pro',
 u'price': 609}
{u'_id': ObjectId('5ad6be71962d7459474c2564'),
 u'client': u'Cody',
 u'item': u'Mac Pro',
 u'price': 1579}
```
