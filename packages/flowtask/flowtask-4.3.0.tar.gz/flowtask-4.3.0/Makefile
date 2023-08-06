venv:
	python3.10 -m venv .venv
	echo 'run `source .venv/bin/activate` to start develop FlowTask'

install:
	pip install --upgrade pip
	pip install wheel==0.38.4
	pip install --upgrade asyncdb[all]
	pip install --upgrade navigator-auth
	pip install --upgrade querysource
	# dev
	python -m pip install -Ur docs/requirements-dev.txt
	# Install extra resources
	pip install --upgrade qworker
	# install FlowTask
	pip install -e .
	echo 'start develop FlowTask'

dev:
	flit install --symlink

release: lint test clean
	flit publish

format:
	python -m black flowtask

distclean:
	rm -rf .venv
