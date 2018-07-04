

> **gitDiffEnhancer 基于git diff 处理增量包**
>

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
![Java v1.8](https://img.shields.io/badge/Java-v1.8.0__162-blue.svg)
![Maven v3.5.3](https://img.shields.io/badge/Maven-v3.5.3-blue.svg)
![Python v3.7](https://img.shields.io/badge/Python-v3.7-blue.svg)


##### 使用方法:
``` powershell
  python gitDiffEnhancer.py --pname=E:\IdeaProjects\kbase-weixin --ocid=02c678b --ncid=f7a4d39
```

##### 参数说明:
> --pname: 项目工作区路径
> --ocid: older commit id
> --ncid:newer commit id

##### 其他说明:
> 1. 基于Maven3+JDK8 测试通过,对IDEA的非实时编译性做了处理
> 2. 使用前先检查 git及mvn命令是否能使用
> 3. pom.xml 需要配置maven-dependency-plugin插件



##### 附

**1. maven-dependency-plugin插件配置Demo**
```
<plugin>
     <groupId>org.apache.maven.plugins</groupId>
     <artifactId>maven-dependency-plugin</artifactId>
     <executions>
         <execution>
             <phase>package</phase>
             <goals>
                 <goal>copy-dependencies</goal>
             </goals>
         </execution>
     </executions>
     <configuration>
         <includeScope>compile</includeScope>
     </configuration>
</plugin>
```