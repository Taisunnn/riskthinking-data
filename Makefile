IMAGE_AIRFLOW=riskthinking-data

DIR=$(shell pwd)

stop:
	docker-compose down

start: stop
	docker-compose --env-file .env up --build

test: stop
	docker build -t $(IMAGE_AIRFLOW) -f Dockerfile .; 
	docker run --rm -t -v $(DIR)/dags:/dags \
		-v $(DIR)/data_in/test:/data_in/test \
		--env-file .env $(IMAGE_AIRFLOW) test

lint: stop
	docker run -ti --rm -v $(DIR):/apps alpine/flake8:3.5.0 --ignore=E501 dags app