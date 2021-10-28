FROM python:3

WORKDIR /usr/src/app

COPY appgoyeneche3.tar.gz ./

RUN tar -xsf appgoyeneche3.tar.gz -C .

WORKDIR /usr/src/app/appgoyeneche3

#COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


#CMD [ "python", "./app.py" ]
CMD ["python", "--version"]
