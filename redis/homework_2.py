import redis
import datetime


ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432

def article_vote(redis, user, article):
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=ONE_WEEK_IN_SECONDS)

    if not datetime.datetime.fromtimestamp(redis.zscore('time:', article)) < cutoff:
        article_id = article.split(':')[-1]
        if redis.sadd('voted:' + article_id, user):
            redis.zincrby(name='score:', value=article, amount=VOTE_SCORE)
            redis.hincrby(name=article, key='votes', amount=1)

def article_switch_vote(redis, user, from_article, to_article):
    # HOMEWORK 2 Part I

    # obtain the ids first
    from_article_id = from_article.split(':')[-1]
    to_article_id   = to_article.split(':')[-1]

    # start a tractional pipeline
    rpipe = redis.pipeline(True)

    # add in commands
    rpipe.zincrby(name='score:', value=from_article, amount=-VOTE_SCORE)
    rpipe.hincrby(name=from_article, key='votes', amount=-1)
    rpipe.srem('voted:' + from_article_id, user)

    rpipe.zincrby(name='score:', value=to_article, amount=VOTE_SCORE)
    rpipe.hincrby(name=to_article, key='votes', amount=1)
    rpipe.sadd('voted:' + to_article_id, user)

    # execute pipeline
    rpipe.execute()

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
# user:3 up votes article:1
article_vote(redis, "user:3", "article:1")
# user:3 up votes article:3
article_vote(redis, "user:3", "article:3")
# user:5 switches their vote from article:1 to article:0
article_switch_vote(redis, "user:2", "article:8", "article:1")

# Which article's score is between 10 and 20?
# PRINT THE ARTICLE'S LINK TO STDOUT:
# HOMEWORK 2 Part II
article = redis.zrangebyscore('score:', 10, 20)
# if there is such an article, just get the first one in case there are many of them
if len(article) > 0:
    article = article[0] 
else:
    print "PART II: no article found. Maybe try reloading the data?"
    import sys
    sys.exit()
article_id = article.split(':')[-1]
print redis.hget("article:" +  article_id, "link")

