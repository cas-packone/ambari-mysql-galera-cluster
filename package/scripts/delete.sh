service mysql stop
rpm -ev galera-3

rpm -ev mysql-wsrep-5.6
rpm -ev mysql-wsrep-client-5.6
rpm -ev mysql-wsrep-server-5.6
rpm -ev boost-program-options

rpm -ev mysql-wsrep-client-5.6-5.6.33-25.17.el6.x86_64                                                                                                                                                               3/5
Irpm -ev mysql-wsrep-5.6-5.6.33-25.17.el6.x86_64                                                                                                                                                                      4/5
rpm -ev galera-3-25.3.18-2.el6.x86_64
#rm -rf /var/lib/mysql
rm -f /etc/mysql/conf.d/my_galera.cnf
