from github import Github
import mysql.connector

cnx = mysql.connector.connect(user='konda',password='password', database='mis_dev_devops')
g = Github("reddy-smhl", "mlp098okn")
for repo in g.get_user().get_repos():
    print("repo_name"+repo.name);
    for j in repo.get_commits():
        committer_name = '' if j.committer is None else str(j.committer.name)
        committer_login = '' if j.committer is None else str(j.committer.login)
        committer_id = '' if j.committer is None else str(j.committer.id)
        committer_updated_at = '' if j.committer is None else str(j.committer.updated_at)
        s = '{"repo_name":"' + repo.name + '","committer_login":"' +committer_login + '","committer_id":"' + str(
            committer_id) + '","committer_name":"' + committer_name + '","updated_date":"' + str(
            committer_updated_at) + '"}'
        print(s)
        cursor = cnx.cursor()
        add_commits = ("INSERT INTO git_repo_commits "
              "(repo_name, committer_login, committer_id, committer_name) "
              "VALUES (%(repo_name)s, %(committer_login)s, %(committer_id)s, %(committer_name)s)")
        # Insert salary information
        data_commits = {
            'repo_name': repo.name, 'committer_login': committer_login, 'committer_id': committer_id, 'committer_name': committer_name }
        cursor.execute(add_commits, data_commits)

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
cnx.close()




