import jenkins
import mysql.connector
import sys


def get_mongodb_con():
    cnx = mysql.connector.connect(host='127.0.0.1',port=3306,user='root', password='root', database='mis_dev_devops')
    return cnx;
def db_jobs_insert(db,job):
    cursor = db.cursor()
    add_jobs = ("INSERT INTO jenkins_jobs "
                   "(job_name, job_url, job_color, job_fullname,job_class) "
                   "VALUES (%(job_name)s, %(job_url)s, %(job_color)s, %(job_fullname)s, %(job_class)s)")
    # Insert salary information
    data_jobs = {
        'job_name': job['name'], 'job_url': job['url'], 'job_color': job['color'],
        'job_fullname': job['fullname'], 'job_class': job['_class']}
    cursor.execute(add_jobs, data_jobs)

    # Make sure data is committed to the database
    db.commit()
    cursor.close()


def get_jenkins_jobs():
    try:
        db=get_mongodb_con()
        jobs = server.get_all_jobs()
        for job in jobs:
            print(job)
            db_jobs_insert(db,job);
            job_name=job['name']
            print(job_name)
            jobs_info = server.get_job_info(job_name)
            if(jobs_info['nextBuildNumber'] > 1):
                last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
                #print(last_build_number)
                build_info = server.get_build_info(job_name, last_build_number)
                #print(build_info)
            #jobs_build_info_id = jobs_build_info_collection.insert_one(build_info).inserted_id

            #print(post_id)
            #print(jobs_info_id)
            #print jobs_build_info_id
    except ValueError:
        print "Error Can't find the input file"
    except:
        print ("Unexcepted Error", sys.exc_info()[0])

    finally:
        print("cleaning")


if(__name__=="__main__"):
    try:
        server = jenkins.Jenkins('http://localhost:8080', username='admin', password='admin')
        user = server.get_whoami()
        version = server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))

        get_jenkins_jobs()
    finally:
        print("cleanup")




