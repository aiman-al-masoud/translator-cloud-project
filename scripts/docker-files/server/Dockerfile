FROM ubuntu
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install nano -y
RUN apt install iputils-ping -y
RUN apt-get install python3 -y
RUN apt-get install git -y
RUN apt install python3-pip -y
RUN git clone https://github.com/aiman-al-masoud/translator-cloud-project.git
RUN apt install python3.10-venv -y
RUN apt install default-libmysqlclient-dev -y
RUN pip3.10 install -r translator-cloud-project/requirements.txt
RUN bash
