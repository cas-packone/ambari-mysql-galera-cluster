mysql  << EOF
SET wsrep_on=OFF;
use mysql;
update user set password=password("galera_password") where user="root";
flush privileges;
quit
EOF
