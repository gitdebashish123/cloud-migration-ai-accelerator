## 🚀 Prerequisites

- Hadoop installed and running (see [README.md](README.md))
- MySQL or MariaDB installed
- Java (OpenJDK 17 or later)
- Environment variables set for Hadoop

---

### 🧩 Step 1: Download MySQL
```bash
brew install MySQL
brew services start 
brew services restart mysql
brew services list
mysql_secure_installation
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