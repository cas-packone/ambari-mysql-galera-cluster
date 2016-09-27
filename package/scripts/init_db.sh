mysql -u root --password=galera_password << EOF
SET wsrep_on=OFF;
use mysql;
update user set password=password("galera_password") where user="root";
GRANT ALL PRIVILEGES ON *.* TO root@localhost  IDENTIFIED BY 'galera_password' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO root@"%"  IDENTIFIED BY 'galera_password' WITH GRANT OPTION;
DELETE FROM mysql.user WHERE user='';
GRANT ALL ON *.* TO 'wsrep_sst-user'@'%' IDENTIFIED BY 'galera_password';
flush privileges;
quit
EOF
