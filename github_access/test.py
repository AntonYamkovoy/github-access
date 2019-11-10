from github import Github
import pymongo
from pymongo import MongoClient



def insert_user(user):
    name = user.name
    location = user.location

    #followers_list = user.followers
    #following_list = user.following
    repositories = user.get_repos()
    # insert user information gathered into db
    db.users.insert_one(
        {
        "name": name,
        "location": location

         })
    for repo in repositories:
        insert_repo(repo)




def insert_repo(repo):


    contributors = repo.get_contributors()
    for contributor in contributors:
        db.contributors.insert_one(
        {
        "repo"  : repo.name,
        "contributors": contributor.name
         })

    commits = repo.get_commits()
    for commit in commits:
            author = commit.commit.author.name
            datetime = commit.commit.author.date
            additions = commit.stats.additions
            deletions = commit.stats.deletions
            total = commit.stats.total
            db.commits.insert_one(
            {
             "repo" : repo.name,
             "author": author,
             "datatime": datetime,
             "size": {"additions": additions, "deletions": deletions, "total": total}
             })


    languages = repo.get_languages()
    
    for language in languages:
        db.language.insert_one(
        {
        "repo"  : repo.name,
        "language": language
         })

    db.repos.insert_one(
        {
         "created": repo.created_at,
         "name": repo.name,
         "description": repo.description

     })


client = pymongo.MongoClient("mongodb+srv://Anton:mongo@sweng-cqjlw.mongodb.net/test?retryWrites=true&w=majority")
g2 = Github("4a78d9e6a5a0602050ccf60acf08cda73c530e96")
#  4a78d9e6a5a0602050ccf60acf08cda73c530e96 github key
user = g2.get_user("yungene")

#inserting collected data into db
db = client.sweng_data
userData = db.users
repoData = db.repos


insert_user(user)





























client.close()
