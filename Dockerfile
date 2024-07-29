FROM python:3.11

LABEL name="doctr"
LABEL version="v1"
 
RUN apt-get update && apt-get install -y 

ENV HOME /home/app
WORKDIR /home/app

COPY requirements.txt .

RUN apt-get update -y
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


EXPOSE 8080



ENTRYPOINT [ "/entrypoint.sh"]