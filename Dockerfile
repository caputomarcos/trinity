FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir git+https://github.com/caputomarcos/trinity.git

ONBUILD COPY . /usr/src/app

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN fabric-bolt init /usr/src/app/settings.py
RUN fabric-bolt --config=/usr/src/app/settings.py migrate
RUN fabric-bolt --config=/usr/src/app/settings.py create_admin

EXPOSE 8000
CMD ["fabric-bolt", "--config=/usr/src/app/settings.py", "runserver", "0.0.0.0:8000"]