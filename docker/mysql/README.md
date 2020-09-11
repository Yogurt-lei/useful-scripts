> mysql 主从

启动完成后

1. 主库: 
```mysql
CREATE USER 'testSyn'@'%' IDENTIFIED BY '123456';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'testSyn'@'%';  
show master status;
```
        
2. 从库: 
       
```mysql
change master to master_host='mysql-master', master_user='testSyn', master_password='123456', master_port=3306, master_log_file='replicas-mysql-bin.000003', master_log_pos=621, master_connect_retry=30;
``` 