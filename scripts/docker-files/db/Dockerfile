FROM ubuntu/mysql:8.0-22.04_beta
RUN apt-get update
RUN apt-get install nano -y
RUN apt install iputils-ping -y
RUN apt-get install python3 -y
RUN apt-get install git -y
RUN apt install python3-pip -y
RUN apt install default-libmysqlclient-dev -y
RUN git clone -n https://github.com/aiman-al-masoud/translator-cloud-project.git --depth 1
WORKDIR translator-cloud-project/scripts
RUN git checkout HEAD init-db.sql
ENTRYPOINT echo "source init-db.sql" | mysql -u root -p"My:S3cr3t/"