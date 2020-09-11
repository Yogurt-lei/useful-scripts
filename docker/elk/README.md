# ELK STACK


启动后 `docker-compose exec -T elasticsearch bin/elasticsearch-setup-passwords auto --batch` 创建默认密码，并保存下来 如下所示
然后更改 kibana.yml logstash.yml logstash.conf 中的elastic的密码为对应密码 

Changed password for user apm_system
PASSWORD apm_system = uPYlhK6iJlMx7gA1U0be

Changed password for user kibana
PASSWORD kibana = 2aDhdbUKNBnRsN23WLs6

Changed password for user logstash_system
PASSWORD logstash_system = k7PJxbNfrFa8EC9fySDq

Changed password for user beats_system
PASSWORD beats_system = zBOwce6CFBmEipOa1GmK

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = IcfpJUlwofTww7DJaWS7

Changed password for user elastic
PASSWORD elastic = k7uPXGn9mWuBiq85COtn