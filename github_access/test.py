from github import Github
import pymongo
from pymongo import MongoClient

import json
import os
import datetime



def reverse_github_results(paginated_list):
    for i in range(paginated_list.totalCount//30, -1, -1):
        page = paginated_list.get_page(i)
        page.reverse()
        for item in page:
            yield item


def insert_user_mod(user):

    count = 0
    login = user.login

    repos = user.get_repos()

    for repo in repos:
        commits = repo.get_commits()
        reverse_github_results(commits)
        print("added suitable commits for repo")
        for commit in commits:
            if count > 100:
                break
            date = commit.commit.author.date
            if date > datetime.datetime(2017,1,1) | date < datetime.datetime(2019,1,1):
                try:

                    db.devs.insert_one(
                            {
                             "login": login,
                             "date" : date,
                             "size" : commit.stats.total

                            })
                    count += 1
                except:
                    print("some error")
        count =0







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









client = pymongo.MongoClient("mongodb+srv://Anton:mongo@sweng-cqjlw.mongodb.net/test?retryWrites=true&w=majority")


g2 = Github("950c09e4661866e9e71bf1ee7fb8939c3a0b8d41")
#  4a78d9e6a5a0602050ccf60acf08cda73c530e96 github key
#950c09e4661866e9e71bf1ee7fb8939c3a0b8d41 sweng 2







#inserting collected data into db
db = client.sweng_data
userData = db.users
repoData = db.repos

db.users.create_index(
    [("login", pymongo.DESCENDING)],
    unique=True
)
db.repos.create_index(
    [("url", pymongo.DESCENDING)],
    unique=True
)

db.commits.create_index(
        [("sha", pymongo.DESCENDING)],
        unique=True

)


usernames = ["edgeui","walterhiggins","vitaly-t"]


for u in usernames:
    user = g2.get_user(u)
    insert_user_mod(user)











# example queries
#     { $and: [ { "language.Java": "Java"},  { url : /yungene/ } ] }
#     {"contributors.AntonYamkovoy": "AntonYamkovoy"}
#
#



















client.close()
