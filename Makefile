init:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

report:
	allure generate allure_results --clean && \
	allure open
