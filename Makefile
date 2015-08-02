root_dir		= $(realpath .)
src_dir			= ${root_dir}/bands

help:
	@echo "Rode make mongo, make export, make import"

kill_mongo:
	@ps aux | awk '(/mongod/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

mongo: kill_mongo
	@rm -rf /tmp/bands/mongodata && mkdir -p /tmp/bands/mongodata
	@mongod --dbpath /tmp/bands/mongodata --logpath /tmp/bands/mongolog --port 7777 --quiet &

mongolog:
	@tail -f /tmp/bands/mongolog

mongoexport:
	@rm -rf /tmp/bands/mongodump && mkdir -p /tmp/bands/mongodump
	@mongoexport -c question -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_question_prod.json
	@mongoexport -c band -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_band_prod.json
	@mongoexport -c user -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_user_prod.json
	@mongoexport -c location -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_location_prod.json
	@mongoexport -c show -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_show_prod.json
	@mongoexport -c newsletter -u heroku -p 9cK3u3i2_3ybKZQQmdUaNy_3tw-A_Uoe9b6g4iHZ7PF_GIYC_UQzrQrtszRZHL3E2y7PGB1qv6ExRjXiloPJgw --host alex.mongohq.com --port 10095 --db app8798964 -o /tmp/bands/mongodump/backup_newsletter_prod.json

mongoimportlocal:
	@mongoimport -c question --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_question_prod.json
	@mongoimport -c band --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_band_prod.json
	@mongoimport -c user --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_user_prod.json
	@mongoimport -c location --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_location_prod.json
	@mongoimport -c show --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_show_prod.json
	@mongoimport -c newsletter --host localhost --port 7777 --db bands --file /tmp/bands/mongodump/backup_newsletter_prod.json

mongodump:
	@make mongo && make mongoexport && make mongoimportlocal

install:
	@pip install -r requirements.txt

clean:
	@find . -type f -name "*.pyc" -exec rm -rf {} \;

kill_run:
	@ps aux | awk '(make run && $$0 !~ /awk/){ system("kill -9 "$$2) }'

run_paralelo: clean
	@foreman start

run: clean
	@python ${root_dir}/bands/app.py

tests: clean
	@touch coverage.xml nosetests.xml .coverage
	@rm coverage.xml nosetests.xml .coverage
	@python ${root_dir}/tests/run.py

aceitacao: clean
	@python ${root_dir}/aceitacao/splinter_test.py
