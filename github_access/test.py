from github import Github
import pymongo
from pymongo import MongoClient



def insert_user(user):
    login = user.login
    location = user.location
    nickname = user.name
    email = user.email
    if email is None:
        email = ""
    if nickname is None:
        nickname = ""
    #followers_list = user.followers
    #following_list = user.following
    repositories = user.get_repos()
    # insert user information gathered into db
    print("inserting user ",user.login)
    db.users.insert_one(
        {
        "login": login,
        "name" : nickname,
        "location": location,
        "email" : user.email


         })
    for repo in repositories:
        insert_repo(repo)




def insert_repo(repo):
    contributors = repo.get_contributors()
    commits = repo.get_commits()
    for commit in commits:
            print("inserting commit ",commit.commit.author.name, " ", commit.commit.author.date)
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
    langList = repo.get_languages()
    contList = repo.get_contributors()
    contDict = {}
    langDict = {}
    for lang in langList:
        langDict[lang] = lang
    for cont in contList:
        contDict[cont.login] = cont.login
    print("inserting repo ",repo.name)
    db.repos.insert_one(
        {

         "created": repo.created_at,
         "name": repo.name,
         "description": repo.description,
         "language" : langDict,
         "contributors": contDict

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
