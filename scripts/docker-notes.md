**You may need to run these with `sudo`.**

# Install docker on Ubuntu

```bash
sudo apt  install docker.io
```

# Stop/restart real local mysql server
```bash
service mysql stop
service mysql status
service mysql start
sudo systemctl daemon-reload
sudo systemctl start docker
```

# Idk what these do frankly ...
```bash
sudo groupadd docker
sudo usermod -aG docker ${USER}
su ${USER}
```

# Pulling an image from dockerhub 
https://hub.docker.com/_/mysql
```bash
sudo docker pull mysql
```

# Running a new container (instance) from an image
```bash
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
```
# Logging into a docker container
```bash
docker exec -it some-mysql bash 
```
# Listing all running containers
```bash
docker ps 
```
# Killing a running container
```bash
docker kill some-mysql 
```
# Removing a container for good
```bash
sudo docker rm -f some-mysql 
```
# Uninstalling freaking docker
```bash
sudo apt-get purge -y docker.io
sudo apt-get autoremove -y --purge docker.io
sudo rm -rf /var/lib/docker /etc/docker
sudo rm /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock
```

# Inspect a docker container
```bash
docker inspect some-mysql
```

# Logging into a running docker container
```bash
docker exec -it some-mysql bash
```

# In mysql shell, to allow remote accesses by root
```bash
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
# Access mysql shell remotely
```bash
mysql -h 172.17.0.2 -P 3306 -u root -p 
# then enter password ...
```

# Copy a file to a docker machine
```bash
docker cp foo.txt container_id:/foo.txt
```

# Path where docker containers are stored
```bash
/var/lib/docker
```

# Running flask app from docker container, accessible from host
```bash
python3 -m flask run --host=0.0.0.0 --port=80
```

# Build custom image from Dockerfile in current dir
```bash
docker build -t nome-immagine .
```

# Empty the cache
```bash
docker system prune -a
```