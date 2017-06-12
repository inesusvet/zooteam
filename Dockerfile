FROM zookeeper

RUN apk add --no-cache python2 py-pip
ADD src/* /usr/local/lib/zooteam/
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
