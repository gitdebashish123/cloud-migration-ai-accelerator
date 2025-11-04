
### 🧩 Step 1: Install OpenJDK 17
```bash
brew install openjdk@17
#Then link it so Java 17 is used system-wide:
sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

#If you need to have openjdk@17 first in your PATH, run:
echo 'export PATH="/usr/local/opt/openjdk@17/bin:$PATH"' >> /Users/debashish/.bash_profile


#Verify installation:
java -version
```

### 🧩 Step 2: Install Hadoop

```bash
cd /Users/debashish/Desktop/2.installations
wget https://downloads.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz
tar -xzf hadoop-3.4.0.tar.gz
sudo mkdir -p /usr/local/opt/hadoop
sudo mv hadoop-3.4.0/* /usr/local/opt/hadoop/
```

### 🧩 Step 4: Set Environment Variables

```bash
# vi ~/.bash_profile 
export HADOOP_HOME=/usr/local/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_LOG_DIR=$HADOOP_HOME/logs
export JAVA_HOME=$(/usr/libexec/java_home -v 17)

export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/*
```


### 🧩 Step 5: Test Installation
```bash
hadoop version
```

### 🧩 Step 6: Create directories 
```bash
mkdir -p ~/hadoop/data/dfs/namenode
mkdir -p ~/hadoop/data/dfs/datanode
```

### ⚙️ Step 7: Update XML configurations

Edit `$HADOOP_CONF_DIR/core-site.xml` and add the following content:

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

Edit `$HADOOP_CONF_DIR/hdfs-site.xml` and add the following content:

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>

  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///Users/debashish/hadoop/data/dfs/namenode</value>
  </property>

  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///Users/debashish/hadoop/data/dfs/datanode</value>
  </property>
</configuration>
```

Edit `$HADOOP_CONF_DIR/mapred-site.xml` and add the following content:

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  
  <property>
  <name>mapreduce.admin.map.child.java.opts</name>
  <value>-XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED</value>
</property>

<property>
  <name>mapreduce.admin.reduce.child.java.opts</name>
  <value>-XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED</value>
</property>


<property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>

  <!-- Ensures mapper tasks get the Hadoop jars -->
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>

  <!-- Ensures reducer tasks get the Hadoop jars -->
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>


</configuration>

```

Edit `$HADOOP_CONF_DIR/yarn-site.xml` and add the following content:

```xml
<?xml version="1.0"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->
<configuration>

<!-- Site specific YARN configuration properties -->
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>


  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
  </property>

  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_HOME,HADOOP_CONF_DIR,PATH,LD_LIBRARY_PATH</value>
  </property>
</configuration>

```

### 🧩 Step 8 : Format HDFS and Start Hadoop in Pseudo-Distributed Mode
```bash
hdfs namenode -format
start-dfs.sh
start-yarn.sh
```

### 🧩 Step 9 : Verify if services are running
```bash
jps

# Output should look like
#28305 Jps
#85200 NodeManager
#85090 ResourceManager
#84630 DataNode
#84520 NameNode
#84776 SecondaryNameNode
```

### 🧩 Step 10: Verify web UIs

 - [NameNode](http://localhost:9870)
 - [SecondaryNameNode](http://localhost:9868)
 - [ResourceManager](http://localhost:8088)

### 🧩 Step 11: Verify sample map reduce job
```bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.0.jar pi 5 10
```