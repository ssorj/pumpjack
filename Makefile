export PYTHONPATH = ${PWD}/python

.PHONY: render-html
render-html: clean
	PYTHONPATH=${PWD}/python scripts/pumpjack -r html -i proton -o input
	transom input output --site-url "file://${PWD}/output"

.PHONY: render-python
render-python: 
	scripts/pumpjack -r python -i proton -o output

.PHONY: help
help:
	@echo "render-html, render-python, clean, publish"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	rm -rf output

.PHONY: publish
publish: temp_dir := $(shell mktemp -d)
publish:
	chmod 755 ${temp_dir}
	transom input ${temp_dir} --site-url "/~jross/pumpjack"
	rsync -av ${temp_dir}/ jross@people.apache.org:public_html/pumpjack
	rm -rf ${temp_dir}

.PHONY: update-pencil
update-pencil:
	curl "https://raw.githubusercontent.com/ssorj/pencil/master/python/pencil.py" -o python/pencil.py
