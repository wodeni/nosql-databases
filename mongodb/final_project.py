# COMS 3102 Final Project
# Wode "Nimo" Ni

# Put the use case you chose here. Then justify your database choice:
# MongoDB
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
#
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
#
#

from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
import re

# setup
client    = MongoClient()
db        = client.db
hn        = db.hackernews
users     = hn.users
posts     = hn.posts
comments  = hn.comments
jobs      = hn.jobs
DEBUG     = True

def clear(db):
    db.command("dropDatabase")

clear(db)

def add_msg(from_user, to_user, content):
    ''' add a private message'''
    result = hn.insert_one({
        'content': title,
        'from': from_user,
        'tro': to_user,
        'created': datetime.now()
    })
    return result.inserted_id

def add_job(title, closed=False):
    ''' add a job to a post by an user'''
    result = jobs.insert_one({
        'title': title,
        'closed': closed,
        'created': datetime.now()
    })
    id = result.inserted_id
    if DEBUG:
        print "Inserted job ID " + str(id)
        result = jobs.find_one({ '_id': result.inserted_id })
        pprint(result)
    return id

def add_vote(user, post):
    ''' add a vote to a post by an user'''
    result = hn.insert_one({ 'user': user, 'post': post })
    id     = result.inserted_id
    update = posts.update_one({ '_id': post }, { '$push': { 'votes': id } })
    if DEBUG:
        print "Modified " +  str(update.modified_count) + " documents"
        doc = posts.find_one({ '_id': post })
        pprint(doc)

def add_comment(user, post, content, replying=None):
    ''' add a comment to the database '''
    result = comments.insert_one({
        'user': user,
        'post': post,
        'replying': replying,
        'content': content,
        'created': datetime.now()
    })
    id = result.inserted_id
    if DEBUG:
        print "Inserted post ID " + str(id)
        result = hn.comments.find_one({ '_id': result.inserted_id })
        pprint(result)
    users.update( { '_id': user }, { '$push': { 'comments': id } } )
    posts.update( { '_id': post }, { '$push': { 'comments': id } } )
    return id

def add_ask(user, title, url='', text=''):
    ''' add a post in the "ask" section '''
    return add_post(user, 'Ask HN: ' + title, url, text)

def add_show(user, title, url='', text=''):
    ''' add a post in the "show" section '''
    return add_post(user, 'Show HN: ' + title, url, text)

def add_post(user, title, url='', text=''):
    ''' add a post to the database and increment karma '''
    assert len(url) != 0 or len(text) != 0

    # add post
    result = posts.insert_one({
        'user': user,
        'title': title,
        'url': url,
        'text': text,
        'votes': [],
        'comments': [],
        'created': datetime.now()
    })
    id = result.inserted_id
    if DEBUG:
        print "Inserted post ID " + str(id)
        result = posts.find_one({ '_id': result.inserted_id })
        pprint(result)

    # increment karma
    users.update(
        { '_id': user },
        {
            '$inc': { 'karma': 1 },
            '$push': { 'posts': id }
        }
    )
    return id

def add_user(name, email, pwd):
    ''' add an user to the database '''
    # insert users
    result = users.insert_one({
        'name': name,
        'email': email,
        'password': pwd,
        'karma': 0,
        'created': datetime.now(),
        'posts': [],
        'comments': []
    })
    id = result.inserted_id
    if DEBUG:
        print "Inserted user ID " + str(id)
        result = users.find_one({ '_id': result.inserted_id })
        pprint(result)
    return id

# add users
if DEBUG: print '\n------------------- Inserting users\n'
nimo = add_user('nimo', 'wn2155@columbia.edu', 'pass')
john = add_user('john', 'john@columbia.edu', 'pass1')
bill = add_user('bill', 'bill@columbia.edu', 'pass2')

# add 5 posts
if DEBUG: print '\n------------------- Inserting posts\n'
add_post(nimo, 'This NoSQL class at Columbia is interesting...',
    url = 'https://github.com/estolfo/nosql-databases')
goto   = add_post(nimo, 'Goto statements considered harmful',
    url = 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf')
victor = add_post(bill, 'VICTOR\'S TECH(?) BLOG',
    url = 'http://www.chengtianxu.com/')
site   = add_post(nimo, 'Nimo\'s official site!',
    url = 'http://www.wodenimoni.com/')
dog    = add_post(john, 'dog video',
    url = 'https://www.youtube.com/watch?v=VrwBnj9myuc')

# add 5 comments
if DEBUG: print '\n------------------- Inserting comments\n'
add_comment(nimo, goto,   'This is visionary!')
add_comment(bill, goto,   'I still use goto all the time : (')
add_comment(john, goto,   'Same here', replying=bill)
add_comment(nimo, victor, 'This is Victor\'s blog, right? Looks good')
add_comment(bill, victor, 'yeah, mine is better', replying=nimo)

# add votes
if DEBUG: print '\n------------------- Upvoting posts\n'
add_vote(nimo, victor)
add_vote(nimo, goto)
add_vote(bill, victor)
add_vote(bill, goto)
add_vote(john, victor)
add_vote(john, dog)

# add 2 jobs
if DEBUG: print '\n------------------- Adding 2 jobs\n'
add_job('Lowest paid software engineer at Columbia University', closed=True)
add_job("A random start-up that sells you to somewhere else")

# add 2 asks
if DEBUG: print '\n------------------- Adding a question\n'
add_ask(bill, "How to set up your github pages?", text="I am so confused")
succeed = add_ask(bill, "How to succeed in college?", text="I am so ambitious.")
add_comment(nimo, succeed, "Don't drink too much.");

# add 2 shows
if DEBUG: print '\n------------------- Adding 2 shows\n'
add_show(nimo, "A C++ library for vector graphics animation!",
    url = 'https://github.com/wodeni/Animate-plus-plus')
add_show(bill, "A deep learning model that authenticates Chinese jades!",
    url = 'https://github.com/xuanyuanzhang/EagleEyes/tree/master/images')

# Action 1: A user publishes an article
print '\n ----- Action 1: A user publishes an article\n'
php    = add_post(bill, 'PHP is the best language',
    text = 'I agree with that statement :P')

# Action 2: A user sees titles of the 10 highest-voted articles
print '\n ----- Action 2: A user sees titles of the 10 highest-voted articles\n'
cursor = posts.aggregate([
    {
        '$project' : {
            'vote_count': { '$size': { "$ifNull": [ "$votes", [] ] } },
            'title': '$title'
         }
    },
    { '$sort': {"vote_count": -1} }
])
i = 0
for document in cursor:
    if i == 10: break
    pprint(document['title'])
    i += 1

# Action 3: A user comments on an article
print '\n ----- Action 3: A user comments on an article\n'
add_comment(john, php, 'I just cannot agree with you. That language sucks!')

# Action 4: A user up-votes an article
print '\n ----- Action 4: A user up-votes an article\n'
add_vote(nimo, php)

# Action 5: A user replies another comment
print '\n ----- Action 5: A user replies another comment\n'
add_comment(bill, php, 'You do not understand PHP. Shame on you', replying=john)

# Action 6: A user sees all jobs that are open
print '\n ----- Action 6: A user sees all jobs that are open\n'
cursor = jobs.find({ 'closed': False })
for document in cursor:
    pprint(document)

# Action 7: A user checks all the shows
print '\n ----- Action 7: A user check all the shows\n'
regx = re.compile(r"^Show HN:")
cursor = posts.find({"title": regx})
for document in cursor:
    pprint(document)

# Action 8: A user check sall the answered asks
print '\n ----- Action 8: A user check all the answered asks\n'
regx = re.compile("^Ask HN:")

cursor = posts.find({"title": regx,  'comments': { '$ne': [] } })
for document in cursor:
    pprint(document)
