from github import Github
import mysql.connector
import json
g = Github("", "")
for repo in g.get_user().get_repos():
     print ("repo name"+repo.name)
     for j in repo.get_commits():
         committer_name='' if j.committer.name is None else str(j.committer.name)
         s = '{"repo_name":"' + repo.name + '","committer_login":"' +  j.committer.login + '","committer_id":"' +  str(j.committer.id)+ '","committer_name":"'+committer_name+ '","updated_date":"'+str(j.committer.updated_at)+ '"}'
         print(json.loads(s))
