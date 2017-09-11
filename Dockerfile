FROM python:2.7

RUN mkdir -p /usr/src/trinity
WORKDIR /usr/src/trinity

RUN pip install --no-cache-dir \
        git+https://github.com/caputomarcos/trinity.git \
    django-debug-toolbar

ONBUILD COPY . /usr/src/trinity

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN fabric-bolt init /usr/src/app/settings.py && \
        fabric-bolt --config=/usr/src/app/settings.py migrate && \
    fabric-bolt --config=/usr/src/app/settings.py create_admin

EXPOSE 8000
CMD ["fabric-bolt", "--config=/usr/src/app/settings.py", "runserver", "0.0.0.0:8000"]