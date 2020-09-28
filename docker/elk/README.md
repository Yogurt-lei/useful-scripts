# ELK STACK


启动后 `docker-compose exec -T elasticsearch bin/elasticsearch-setup-passwords auto --batch` 创建默认密码，并保存下来 如下所示
然后更改 kibana.yml logstash.yml logstash.conf 中的elastic的密码为对应密码, 然后restart

Changed password for user apm_system
PASSWORD apm_system = oEtQTZzze2gdojJxZm0U

Changed password for user kibana
PASSWORD kibana = gpJVMEq9uXuG5EyXOVaw

Changed password for user logstash_system
PASSWORD logstash_system = oGUIWhGECFmCr87VvSs2

Changed password for user beats_system
PASSWORD beats_system = 9b4s8ImcsjAz9GKIlK8s

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = YU6uSl7HpIakl2VPeXwb

Changed password for user elastic
PASSWORD elastic = W1QqYDqf7gxwuCqfTS8l