from github import Github



g = Github("4a78d9e6a5a0602050ccf60acf08cda73c530e96")

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
