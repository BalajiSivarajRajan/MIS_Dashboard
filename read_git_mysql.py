from github import Github
import mysql.connector

cnx = mysql.connector.connect(user='',password='', database='mis_dev_devops')
g = Github("", "")
for repo in g.get_user().get_repos():
    print("repo_name"+repo.name);

    for j in repo.get_commits():
        if(j.committer is not None):
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
              "(repo_name, committer_login, committer_id, committer_name,updated_date) "
              "VALUES (%(repo_name)s, %(committer_login)s, %(committer_id)s, %(committer_name)s, %(updated_date)s)")
            # Insert salary information
            data_commits = {
            'repo_name': repo.name, 'committer_login': committer_login, 'committer_id': committer_id, 'committer_name': committer_name, 'updated_date':committer_updated_at }
            cursor.execute(add_commits, data_commits)

            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()



    max_pull_number=1
    for k in repo.get_pulls():
        max_pull_number=k.number
    print("max_pull_number:"+str(max_pull_number))
    if(max_pull_number > 1):
        pull_iter=1
        while(pull_iter<=max_pull_number):
            pull=repo.get_pull(pull_iter)
            s = '{"repo_name":"' + repo.name + '","committer_login":"' + pull.user.login+'","repo_pull_id":"' + str(pull.id) +'","title":"' + pull.title+'","state":"' + pull.state+'","created_time":"' + str(pull.created_at)+'","additions":"' + str(pull.additions)+'","deletions":"' + str(pull.deletions)+'"}'
            print(s)
            cursor = cnx.cursor()
            add_pulls = ("INSERT INTO git_repo_pulls "
                           "(repo_name, committer_login, repo_pull_id, title,state,repo_pull_created_time,additions,deletions) "
                           "VALUES (%(repo_name)s, %(committer_login)s, %(repo_pull_id)s, %(title)s, %(state)s, %(repo_pull_created_time)s, %(additions)s, %(deletions)s)")
            # Insert salary information
            data_pulls = {
                'repo_name': repo.name, 'committer_login': pull.user.login, 'repo_pull_id': str(pull.id),
                'title': pull.title, 'state': pull.state, 'repo_pull_created_time': str(pull.created_at),'additions': str(pull.additions),'deletions': str(pull.deletions)}
            cursor.execute(add_pulls, data_pulls)

            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            pull_iter=pull_iter+1




    max_number=0
    for issue in repo.get_issues():
        if (issue.number > max_number):
            max_number = issue.number
    if(max_number > 0):
        iter1 = 1
        while (iter1 <= max_number):
            issue = repo.get_issue(iter1)
            s = '{"repo_name":"' + repo.name + '","issue_user":"' + issue.user.login + '","repo_issue_id":"' + str(
                issue.id) + '","title":"' + issue.title + '","state":"' + issue.state + '","created_time":"' + str(
                issue.created_at) + '"}'
            print(s)
            cursor = cnx.cursor()
            add_issues = ("INSERT INTO git_repo_issues "
                         "(repo_name, issue_user, repo_issue_id, title,state,repo_issue_created_time) "
                         "VALUES (%(repo_name)s, %(issue_user)s, %(repo_issue_id)s, %(title)s, %(state)s, %(repo_issue_created_time)s)")
            # Insert salary information
            data_issues = {
                'repo_name': repo.name, 'issue_user': issue.user.login, 'repo_issue_id': str(issue.id),
                'title': issue.title, 'state': issue.state, 'repo_issue_created_time': str(issue.created_at)}
            cursor.execute(add_issues, data_issues)

            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            iter1 = iter1 + 1



cnx.close()