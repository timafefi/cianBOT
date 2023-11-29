FROM python:3.10

WORKDIR /home


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./ /home/
RUN useradd -ms /bin/bash admin
RUN chown -R admin:admin /home/
RUN pip install -r /home/requirements.txt && apt-get update
USER admin
ENV PYTHONPATH /home/
ENV PATH=$PATH:/home/

ENTRYPOINT ["python", "main.py"]

