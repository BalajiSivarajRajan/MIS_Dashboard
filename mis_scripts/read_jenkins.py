import jenkins
import mysql.connector
import sys


def get_mysqldb_con():
    cnx = mysql.connector.connect(host='127.0.0.1',port=3306,user='grafana', password='password', database='mis_dev_devops')
    return cnx;
def db_jobs_insert(db,job,build):
    cursor = db.cursor()
    add_jobs = ("INSERT INTO jenkins_jobs "
                   "(job_name, job_url, job_color, job_fullname,job_class,build_timestamp,build_number,build_result,build_duration) "
                   "VALUES (%(job_name)s, %(job_url)s, %(job_color)s, %(job_fullname)s, %(job_class)s, FROM_UNIXTIME(%(build_timestamp)s), %(build_number)s, %(build_result)s, %(build_duration)s )")
    # Insert salary information
    k=build['timestamp'] / 1000
    print("k:"+str(k))
    data_jobs = {
        'job_name': job['name'], 'job_url': job['url'], 'job_color': job['color'],
        'job_fullname': job['fullname'], 'job_class': job['_class'], 'build_timestamp': build['timestamp'] / 1000,
        'build_number': build['number'], 'build_result': build['result'], 'build_duration': build['duration']}
    cursor.execute(add_jobs, data_jobs)

    # Make sure data is committed to the database
    db.commit()
    cursor.close()


def get_jenkins_jobs():
    try:
        db=get_mysqldb_con()
        jobs = server.get_all_jobs()
        for job in jobs:
            print(job)
            job_name=job['name']
            print(job_name)
            jobs_info = server.get_job_info(job_name)
            #print(jobs_info)
            if(jobs_info['nextBuildNumber'] > 1):
                last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
                #print(last_build_number)
                iter=1
                while(iter <= last_build_number):
                    build_info = server.get_build_info(job_name, iter)
                    db_jobs_insert(db, job,build_info);
                    print(build_info['timestamp'])
                    print(build_info['number'])
                    print(build_info['result'])
                    print(build_info['duration'])
                    iter = iter + 1;




    except ValueError:
        print "Error Can't find the input file"
    except:
        print ("Unexcepted Error", sys.exc_info()[0])

    finally:
        print("cleaning")


if(__name__=="__main__"):
    try:
        #server = jenkins.Jenkins('http://localhost:8080', username='admin', password='admin')
        server = jenkins.Jenkins('http://35.177.162.4:8080', username='admin', password='admin')
        get_jenkins_jobs()
    finally:
        print("cleanup")





