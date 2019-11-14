from github import Github
import pymongo
from pymongo import MongoClient



def insert_user(user):
    login = user.login
    location = user.location
    nickname = user.name
    email = user.email
    followerList = user.get_followers()
    followingList = user.get_following()

    followers = {}
    following = {}
    if email is None:
        email = ""
    if nickname is None:
        nickname = ""
    for f in followers:
        followers[f.login] = f.login

    for f in following:
        following[f.login] = f.login




    # insert user information gathered into db
    print("inserting user ",user.login)
    db.users.insert_one(
        {
        "login": login,
        "name" : nickname,
        "location": location,
        "email" : user.email,
        "following" : following,
        "followers" : followers


         })
    repositories = user.get_repos()
    for repo in repositories:
        insert_repo(repo)




def insert_repo(repo):
    contributors = repo.get_contributors()
    commits = repo.get_commits()
    commitDict = {}

    for commit in commits:
            #print("inserting commit ",commit.commit.author.name, " ", commit.commit.author.date)
            commitDict[commit.sha] = (commit.commit.author.name, commit.commit.author.date, commit.stats.additions, commit.stats.deletions, commit.stats.total)
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
         "contributors": contDict,
         "commits" : commitDict

     })




client = pymongo.MongoClient("mongodb+srv://Anton:mongo@sweng-cqjlw.mongodb.net/test?retryWrites=true&w=majority")
g2 = Github("4a78d9e6a5a0602050ccf60acf08cda73c530e96")
#  4a78d9e6a5a0602050ccf60acf08cda73c530e96 github key
user = g2.get_user("AntonYamkovoy")


#inserting collected data into db
db = client.sweng_data
userData = db.users
repoData = db.repos


insert_user(user)



































client.close()
