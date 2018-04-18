# COMS 3102 Homework 3 solution

from pymongo import MongoClient

# setup
client = MongoClient()
db     = client.db
movies = db.movies

# Part A
print "\nPart A\n"

result = movies.update_many(
    { 
        'rated': 'NOT RATED',
        'genres': 'Comedy'
    }, 
    {
        '$set':  { 'rated': 'Pending rating' } 
    }
)
print "Modified " +  str(result.modified_count) + " documents" # printed 508 for the first time


# Part B
print "\nPart B\n"

result = movies.insert_one({
    'title': 'Love, Simon',
    'year' : 2018,
    'countries': [ 'USA' ],
    'genres': [ 'Comedy', 'Drama', 'Romance' ] ,
    'directors': [ 'Greg Berlanti' ],
    'imdb': {
        'id': 5164432,
        'rating': 8.1,
        'votes': 13767,
    }
})
print "Inserted ID " +  str(result.inserted_id) 
result = movies.find_one({ '_id': result.inserted_id })
print result

# Part C
print "\nPart C\n"

cursor = movies.aggregate(
    [ 
        {'$match': { 'genres': 'Comedy' } },
        {'$group': { '_id': 'Comedy', "count": {"$sum": 1} }}
    ]
)

print "Counting the number of Comedy movies: "
for document in cursor:
    print document

# Part D
print "\nPart D\n"

cursor = movies.aggregate([ 
    {'$match': { 'countries': 'China', 'rated': 'Pending rating' } },
    {'$group': 
        { 
            '_id': { 'countries': 'China', 'rated': '$rated' } , 
            "count": {"$sum": 1} 
        }
    }
])

print "Counting the number of unrated Chinese movies: "
for document in cursor:
    print document

# Part E
print "\nPart E\n"

# Creat two collections
purchases = db.purchases
prices    = db.prices
purchases.insert_many([
    { 'client': 'Bob', 'item': 'iPhone X' },
    { 'client': 'Alice', 'item': 'iPad Pro' },
    { 'client': 'Cody', 'item': 'Mac Pro' },
])
prices.insert_many([
    { 'name': 'iPhone X', 'price': 999  },
    { 'name': 'Mac Pro',  'price': 1579 },
    { 'name': 'iPad Pro', 'price': 609  }
])

# "join" the two collections via the common item column

cursor = purchases.aggregate([
    { '$lookup': 
        {
            'from': 'prices',
            'localField': 'item',
            'foreignField': 'name',
            'as': 'price_info'
        }
    },
    { '$project': 
        {
            'client': 1,
            'item': 1,
            'price': '$price_info.price'
        }
    }
])

for document in cursor:
    try:
        from pprint import pprint
        pprint(document)
    except ImportError:
        print document
