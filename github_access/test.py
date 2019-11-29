from github import Github
import pymongo
from pymongo import MongoClient

import json
import os
import datetime


lat = 0
long = 0






def reverse_github_results(paginated_list):
    for i in range(paginated_list.totalCount//30, -1, -1):
        page = paginated_list.get_page(i)
        page.reverse()
        for item in page:
            yield item





""""
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
    for f in followerList:
        followers[f.node_id] = (f.login)

    for f in followingList:
        following[f.login] = (f.login)




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
       try:
               insert_repo(repo)
       except:
           print("duplicate repo spotted E11000")


    for f2 in followingList:
            try:
                insert_user(f2)
            except:
                print("duplicate following spotted E11000")


    for f in followerList:
            try:
                insert_user(f)
            except:
                print("duplicate follower spotted E11000")





"""
"""
def insert_repo(repo):

    commits = repo.get_commits()
    commitDict = {}

    for commit in commits:
            #print("inserting commit ",commit.commit.author.name, " ", commit.commit.author.date)
            commitDict[commit.sha] = (commit.commit.author.name, commit.commit.author.date, commit.stats.additions, commit.stats.deletions, commit.stats.total)
    langList = repo.get_languages()
    contList = repo.get_contributors()
    contDict = {}
    langDict = {}
    name = repo.name
    for lang in langList:
        langDict[lang] = lang
    for cont in contList:
        contDict[cont.login] = cont.login
    print("inserting repo ",name)


    db.repos.insert_one(
        {
         "url": repo.url,
         "created": repo.created_at,
         "name": name,
         "description": repo.description,
         "language" : langDict,
         "contributors": contDict,
         "commits" : commitDict

        })

"""

def get_links(string):
    user = g2.get_user(string)
    repos = user.get_repos()
    #print(user.name)
    for r in repos:
        string = user.login+"/"+r.name
        db.repo_links.insert_one({ "link" : string })




def insert_repo(repo):
    name = repo.name
    try:
        db.repos_new.insert_one({ "name" : name })
    except:
        print("error inserting repo ", name)



    languages = repo.get_languages()
    contributors = repo.get_contributors()
    commits = repo.get_commits()
    for lang in languages:
        insert_language(lang,name)
    for commit in commits:
        insert_commit(commit,name)
    for contributor in contributors:
        insert_user(contributor)


def insert_language(lang,name):
    try:
        db.languages_new.insert_one({  "name" : name,"language" : lang  })
    except:
        print("inserting lang error ",name, " ",lang)



def insert_user(contributor):
    try:
        db.users_new.insert_one({ "login" : contributor.login })
    except:
        print("error ins user ", contributor)


def insert_commit(commit,name):
    try:
        if commit.author is not None:
            date_time = commit.commit.author.date.strftime("%Y:%m:%d:%H:%M:%S")
            print("date ",date_time)
            print("commit author ", commit.author.login)
            db.commits_new.insert_one({ "login" : commit.author.login,  "repo_name" : name, "date": date_time, "sha": commit.sha  })
        else:
            print("inserting commit error", commit.commit.author.name)
    except:
        print(" error in commit ",commit)


reposList = ["flutter-webrtc","flutter_barcode_reader","flutter-nfc-reader","flutterlocation","admob_flutter"]




//client = pymongo.MongoClient("mongodb+srv://Anton:<password>@sweng-cqjlw.mongodb.net/test?retryWrites=true&w=majority")



g2 = "your api key"







#inserting collected data into db
db = client.sweng_data
userData = db.users_new
repoData = db.repos_new
commitsData = db.commits_new
langData = db.languages_new
repList = db.repo_links

db.users_new.create_index(
    [("login", pymongo.DESCENDING)],
    unique=True
)


db.repos_new.create_index(
    [("name", pymongo.DESCENDING)],
    unique=True
)

"""
db.commits_new.create_index(
    [("login", pymongo.DESCENDING),("date", pymongo.DESCENDING)],
    unique=True
)
"""
db.commits_new.create_index(
    [("sha", pymongo.DESCENDING)],
    unique=True
)

db.repo_links.create_index(
    [("link", pymongo.DESCENDING)],
    unique=True
)



db.languages_new.create_index(
    [("name", pymongo.DESCENDING),("language", pymongo.DESCENDING)],
    unique=True
)









"""

userList= []
query = db.users_new.find()
for i in query:
    userList.append(i["login"])


"""

"""
for userStr in userList:
    try:
        get_links(userStr)
    except:
        print("error links",user)

"""
linksList = []
queryLinks = db.repo_links.find()
for i in queryLinks:
    linksList.append(i["link"])


for str in linksList:
    repo = g2.get_repo(str)
    print("adding repo ",str )
    insert_repo(repo)













# example queries
#     { $and: [ { "language.Java": "Java"},  { url : /yungene/ } ] }
#     {"contributors.AntonYamkovoy": "AntonYamkovoy"}
#
#



















client.close()
