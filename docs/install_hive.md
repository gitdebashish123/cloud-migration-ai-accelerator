### 🚀 Prerequisites

👉  [Hadoop Installation Guide](install_hadoop.md)

---

### 🧩 Step 1: Download MySQL
```bash
brew install MySQL
brew services start 
brew services restart mysql
brew services list
mysql_secure_installation
# NOTE - Set up onetime password which will be used in hive-site.xml  
# Replace MySQLPassword for javax.jdo.option.ConnectionPassword
```

### 🧩 Step 2: Set up MySQL for Hive
~~~~sql
DROP DATABASE metastore;
CREATE DATABASE metastore;
CREATE USER 'hiveuser'@'localhost' IDENTIFIED BY 'Hive@1989';
GRANT ALL PRIVILEGES ON metastore.* TO 'hiveuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
~~~~

### 🧩 Step 3: Download Hive

```bash
mkdir ~/Desktop/hadoop-installations
cd ~/Desktop/hadoop-installations

#brew install apache-hive

#manually
wget https://archive.apache.org/dist/hive/hive-4.0.0/apache-hive-4.0.0-bin.tar.gz
tar -xvf apache-hive-4.0.0-bin.tar.gz
```

### 🧩 Step 4: Download Hive

```bash
mkdir ~/Desktop/hadoop-installations
cd ~/Desktop/hadoop-installations

#brew install apache-hive

#manually
wget https://archive.apache.org/dist/hive/hive-4.0.0/apache-hive-4.0.0-bin.tar.gz
tar -xvf apache-hive-4.0.0-bin.tar.gz
```

### 🧩 Step 5: Move the packages to hive folder
```bash
sudo mkdir -p /usr/local/opt/hive
sudo mv apache-hive-4.0.0-bin/* /usr/local/opt/hive/
```

### 🧩 Step 6: Move the packages to hive folder
```bash
sudo mkdir -p /usr/local/opt/hive
sudo mv apache-hive-4.0.0-bin/* /usr/local/opt/hive/
```
### 🧩 Step 7: ~/.bash_profile env set up
```bash
vi ~/.bash_profile
export HIVE_HOME=/usr/local/opt/hive
export HIVE_LOG_DIR=/usr/local/opt/hive/logs
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/*

# Optional but helps for logs
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HIVE_AUX_JARS_PATH=$HIVE_HOME/lib

```

### ⚙️ Step 8: Update hive-site.xml

Edit `$HIVE_HOME/conf/hive-site.xml` and add the following content:

```xml
<?xml version="1.0"?>
<configuration>

  <!-- Hive Metastore connection -->
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <!--<value>jdbc:mysql://localhost:3306/metastore?createDatabaseIfNotExist=true&amp;useSSL=false</value>-->
    <value>jdbc:mysql://localhost:3306/metastore?createDatabaseIfNotExist=true&amp;useSSL=false&amp;allowPublicKeyRetrieval=true</value>
    <description>JDBC connect string for MySQL metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.cj.jdbc.Driver</value>
  </property>

  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hiveuser</value>
  </property>

  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>MySQLPassword</value>
  </property>

  <!-- Warehouse Directory -->
  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
  </property>

  <!-- Metastore Thrift service -->
  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://localhost:9083</value>
  </property>

  <property>
    <name>hive.metastore.event.db.notification.api.auth</name>
    <value>false</value>
  </property>
  
  <!-- disable impersonation in HiveServer2 -->
  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>


  <property>
    <name>hive.server2.thrift.bind.host</name>
    <value>127.0.0.1</value>
  </property>

  <property>
    <name>hive.server2.thrift.port</name>
    <value>10000</value>
  </property>
</configuration>
```

### ⚙️ Step 9: Update hive-env.sh

Edit `$HIVE_HOME/conf/hive-env.sh` and add the following content:
```bash
export HIVE_HOME=/usr/local/opt/hive
export HIVE_LOG_DIR=$HIVE_HOME/logs
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HADOOP_HOME=/usr/local/opt/hadoop
#export HADOOP_CLIENT_OPTS="-Dhive.root.logger=INFO,FILE -Dhive.log.dir=$HIVE_LOG_DIR"
export HADOOP_CLIENT_OPTS="$HADOOP_CLIENT_OPTS -Dhive.log.dir=$HIVE_LOG_DIR -Dhive.root.logger=INFO,console"
export HADOOP_OPTS="$HADOOP_OPTS \
--add-opens=java.base/java.lang=ALL-UNNAMED \
--add-opens=java.base/java.lang.reflect=ALL-UNNAMED \
--add-opens=java.base/java.io=ALL-UNNAMED \
--add-opens=java.base/java.util=ALL-UNNAMED \
--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED \
--add-opens=java.base/sun.nio.ch=ALL-UNNAMED"
```

### ⚙️ Step 9: Update hive-log4j2.properties

Edit `$HIVE_HOME/conf/hive-log4j2.properties` and add the following content:
```bash
status = WARN
name = HiveLog4j2

property.hive.log.dir = ${sys:hive.log.dir}
property.hive.log.file = hive.log

appender.console.type = Console
appender.console.name = Console
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{ISO8601} %-5p [%t] %c{2}: %m%n

appender.file.type = File
appender.file.name = File
appender.file.fileName = /usr/local/opt/hive/logs/hive.log
appender.file.layout.type = PatternLayout
appender.file.layout.pattern = %d{ISO8601} %-5p [%t] %c{2}: %m%n
#rootLogger.level = INFO
rootLogger.level = WARN
rootLogger.appenderRefs = console, file
rootLogger.appenderRef.console.ref = Console
rootLogger.appenderRef.file.ref = File
```

### 🧩 Step 10: Download mysql-connector

```bash
cd ~/Desktop/hadoop-installations
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.4.0.tar.gz
tar -xzf mysql-connector-j-8.4.0.tar.gz
cp mysql-connector-j-8.4.0/mysql-connector-j-8.4.0.jar $HIVE_HOME/lib/
```