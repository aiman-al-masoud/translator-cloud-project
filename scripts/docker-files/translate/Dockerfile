FROM ubuntu
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install nano -y
RUN apt install iputils-ping -y
RUN apt-get install python3 -y
RUN apt-get install git -y
RUN apt install python3-pip -y
RUN git clone https://github.com/aiman-al-masoud/translator-cloud-project.git
WORKDIR translator-cloud-project
RUN git pull
RUN pip3.10 install flask
RUN pip3.10 install argostranslate
RUN pip3.10 install flask_cors
RUN pip3.10 install jsonify
WORKDIR scripts
RUN python3 install-language-models.py -f it -t en -txt "Ciao Mondo"
RUN python3 install-language-models.py -f en -t it -txt "Hello World"
WORKDIR ../
ENTRYPOINT python3 -m src.translate.app
