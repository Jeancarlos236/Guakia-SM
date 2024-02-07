FROM python:3.10

RUN apt-get update && apt-get install -y libsystemd-dev && apt-get -y install python3-systemd 

COPY . /sm_backend

WORKDIR /sm_backend

RUN  pip install dbus-next && pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
