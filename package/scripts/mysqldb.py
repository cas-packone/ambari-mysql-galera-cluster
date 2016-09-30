#coding=utf-8
import os
import base64
from time import sleep
from resource_management import *
from GrantTables import *


class MysqldbMaster(Script):
    mysqldb_packages = ['mysql-wsrep-5.6','galera-3']
    db_pass_file = '/etc/db_info.cnf'

    def install(self, env):
        import params
        #make galera yum resources
        Execute('touch /etc/yum.repos.d/galera.repo ', ignore_failures=True)
        galera_repo = InlineTemplate(params.galera_repo)
        File(format('/etc/yum.repos.d/galera.repo'), content=galera_repo, owner='root')

        # delete mysql-server
        Execute('rpm -e mysql-server', ignore_failures=True)

        #delete yum mysql
        Execute('yum -y remove mysql-libs-*', ignore_failures=True)
        sleep(10)
        Execute('yum clean all ', ignore_failures=True)
        #delete default mysql directory
        Execute('rm -rf /usr/share/mysql', ignore_failures=True)
        #Execute('rm -rf /var/lib/mysql', ignore_failures=True)
        Execute('rm -f /etc/mysql/conf.d/my_galera.cnf', ignore_failures=True)

        self.install_packages(env)
        #print 'install mysqldb'
        #if self.mysqldb_packages is not None and len(self.mysqldb_packages):
        #    for pack in self.mysqldb_packages:
        #       Package(pack)
        #       sleep(10)

        # configure cluster
        Execute('yes | yum install galera-3 mysql-wsrep-5.6')

        sleep(5)
        GrantTables.StartGrantTables()
        sleep(5)

        #set passeord
        self.initdbpwd(env)
        sleep(5)
        Execute('service mysql stop')
        sleep(5)
        Execute('service mysql start')

        #install mysql DB
        self.installDB(env)

        # init db 修改权限和口令
        self.initdb(env)
        sleep(5)
        Execute('service mysql stop')
        sleep(5)

        #创建mysql的配置文件
        Execute('mkdir -p /etc/mysql/conf.d')
        Execute('touch /etc/mysql/conf.d/my_galera.cnf ', ignore_failures=True)

        # 设置
        if not os.path.isfile("/etc/my.cnf"):
            my_cnf = InlineTemplate(params.my_cnf)
            File(format("/etc/my.cnf"), content=my_cnf, owner='root')



    def configure(self, env):
        print 'configure mysqldb'
        import params
        self.installDB(env)

        env.set_params(params)
        server_cnf_content = InlineTemplate(params.server_cnf_content)
        File(format("/etc/mysql/conf.d/my_galera.cnf"), content=server_cnf_content, owner='root')

        db_password = params.db_password
        file_object = open(self.db_pass_file)
        try:
            file_content = file_object.read()
            pre_pass = base64.decodestring(file_content)
            print pre_pass
            if db_password != pre_pass:
                if params.mysqldb_current_host == params.mysqldb_hosts[0]:
                    Execute('/etc/init.d/mysql start --wsrep-new-cluster')
                    cmd = format("/usr/bin/mysqladmin -u root -p{pre_pass} password '{db_password}'")
                    Execute(cmd)
                else:
                    sleep(10)
                    Execute('service mysql start')
                self.initdb(env)
                if params.mysqldb_current_host == params.mysqldb_hosts[0]:
                    self.stop(env)

        finally:
            file_object.close()

    def installDB(self,env):
        print 'install MysqlDB'
        import params
        # init datadir
        db_dir = params.db_dir
        if os.path.exists(db_dir):
            print "Dir exists"
        else:
            Execute(format('mkdir -p {db_dir}'), logoutput=True)
            Execute(format('chown -R mysql:mysql {db_dir}'), logoutput=True)
            Execute(format('mysql_install_db --user=mysql --ldata={db_dir}'), logoutput=True)


    def start(self, env):
        self.configure(env)
        import params
        if params.mysqldb_current_host == params.mysqldb_hosts[0]:
            Execute('/etc/init.d/mysql start --wsrep-new-cluster')
        else:
            sleep(10)
            Execute('service mysql start')

    def stop(self, env):
        Execute('service mysql stop')

    def restart(self, env):
        print("restart")
        self.stop(env)
        self.start(env)

    def status(self, env):
        Execute('service mysql status')

    def initdb(self, env):
        import params;
        env.set_params(params)
        service_packagedir = params.service_packagedir
        init_lib_path = service_packagedir + '/scripts/init_db.sh'
        File(init_lib_path,
             content=Template("init_lib.sh.j2"),
             mode=0777
             )
        cmd = format("{service_packagedir}/scripts/init_db.sh")
        Execute('echo "Running ' + cmd + '" as root')
        Execute(cmd)
        db_pass_file = self.db_pass_file
        cmd = format("rm -rf {db_pass_file}")
        Execute('echo "Running ' + cmd + '" as root')
        Execute(cmd)

        db_password = base64.encodestring(params.db_password)
        File(self.db_pass_file,
             content=db_password,
             mode=0644
             )

    def initdbpwd(self, env):
        import params;
        env.set_params(params)
        service_packagedir = params.service_packagedir
        init_lib_path = service_packagedir + '/scripts/init_db_pwd.sh'
        File(init_lib_path,
             content=Template("init_db_pwd.sh.j2"),
             mode=0777
             )
        cmd = format("{service_packagedir}/scripts/init_db_pwd.sh")
        Execute('echo "Running ' + cmd + '" as root')
        Execute(cmd)



if __name__ == "__main__":
    MysqldbMaster().execute()
