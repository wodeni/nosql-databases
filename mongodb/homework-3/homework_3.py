# COMS 3102 Homework 3 solution

from pymongo import MongoClient

# setup
client = MongoClient()
db     = client.db
movies = db.movies

# Part A

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

# Part C

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

# Part A
