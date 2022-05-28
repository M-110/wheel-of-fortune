.PHONY: test, rate, clean

test:
	poetry run pytest -xvv tests

rate:
	poetry run flake8 wheel_of_fortune
	poetry run pylint wheel_of_fortune

clean:
	poetry run yapf wheel_of_fortune --recursive --in-place --style google
