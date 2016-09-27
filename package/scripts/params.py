from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket
from resource_management.libraries.functions.version import format_hdp_stack_version
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

db_dir=default('configurations/mysqldb/db_path', '/var/lib/mysql')
db_password=default('configurations/mysqldb/db_password', 'dbpass')
#e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.3/services/SOLR/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
mysqldb_hosts = config['clusterHostInfo']['mysqldb_node_hosts']
mysqldb_hosts_str = ','.join(mysqldb_hosts)
mysqldb_current_host = socket.getfqdn(socket.gethostname())
server_cnf_content = config['configurations']['mysqldb']['content']

######################################################################
#yum galera resources
######################################################################
galera_repo = config['configurations']['galera-repo']['content']

######################################################################
#Mysql my.cnf
######################################################################
my_cnf = config['configurations']['mysqldb']['mycnf']

######################################################################
#mysql root user default password
######################################################################
default_pwd = ""
file_object = open("/root/.mysql_secret")
try:
    file_content = file_object.read()
    array = file_content.split(':')
    size = len(array)
    default_pwd = array[size-1]
finally:
    file_object.close()