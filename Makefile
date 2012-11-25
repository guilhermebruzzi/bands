root_dir		= $(realpath .)
src_dir			= ${root_dir}/bands

kill_mongo:
	@ps aux | awk '(/mongod/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

mongo: kill_mongo
	@rm -rf /tmp/bands/mongodata && mkdir -p /tmp/bands/mongodata
	@mongod --dbpath /tmp/bands/mongodata --logpath /tmp/bands/mongolog --port 7777 --quiet &

install:
	@pip install -r requirements.txt

clean:
	@find . -type f -name "*.pyc" -exec rm -rf {} \;

run: clean
	@python ${root_dir}/bands/app.py

tests: clean
	@touch coverage.xml nosetests.xml .coverage
	@rm coverage.xml nosetests.xml .coverage
	@python ${root_dir}/tests/run.py

aceitacao: clean
	@make run &
	@python ${root_dir}/aceitacao/splinter_test.py
	@ps aux | awk '(make run && $$0 !~ /awk/){ system("kill -9 "$$2) }'
