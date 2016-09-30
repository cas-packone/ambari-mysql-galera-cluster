mysql -uroot -padmin  << EOF
SET PASSWORD = PASSWORD('admin');
SET wsrep_on=OFF;
use mysql;
GRANT ALL PRIVILEGES ON *.* TO root@localhost  IDENTIFIED BY 'admin' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO root@"%"  IDENTIFIED BY 'admin' WITH GRANT OPTION;
DELETE FROM mysql.user WHERE user='';
GRANT ALL ON *.* TO 'wsrep_sst-user'@'%' IDENTIFIED BY 'admin';
flush privileges;
quit
EOF
