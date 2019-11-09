from github import Github
import pymongo
from pymongo import MongoClient



client = pymongo.MongoClient("mongodb+srv://Anton:mongo@sweng-cqjlw.mongodb.net/test?retryWrites=true&w=majority")
db = client.sweng_data

posts = db.posts
post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Anton'
}
result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))

client.close()




g = Github("4a78d9e6a5a0602050ccf60acf08cda73c530e96")
#  4a78d9e6a5a0602050ccf60acf08cda73c530e96 github key
user = g.get_user("AntonYamkovoy")
repos = user.get_repos()

for repo in repos:
	print(">",repo.name)
	collaborators = repo.get_contributors()
	for c in collaborators:
		print(">>",c.login)

"""
repo_name = 'bitcoin/bitcoin'
repo = g.get_repo(repo_name)
collaborators = repo.get_collaborators()

for collaborator in collaborators:
    print(collaborator.login)
	"""




print("public: ",user.public_repos, " private: ",user.total_private_repos)
