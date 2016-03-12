export PYTHONPATH = ${PWD}/python

.PHONY: render
render: clean
	scripts/pumpjack -r html -i api -o input
	transom input output

.PHONY: render-python
render-python: 
	scripts/pumpjack -r python -i api -o input/python
	transom input output

.PHONY: help
help:
	@echo "render, render-python, clean, publish"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	rm -rf output

.PHONY: publish
publish: temp_dir := $(shell mktemp -d)
publish: temp_script := $(shell mktemp)
publish: render
	chmod 755 ${temp_dir}
	transom input ${temp_dir} --site-url "/~jross/pumpjack"
#	rsync -av ${temp_dir}/ jross@people.apache.org:public_html/pumpjack
#	rsync -av ${temp_dir}/ jross@home.apache.org::public_html/pumpjack
	echo 'lcd ${temp_dir}' >> ${temp_script}
	cd ${temp_dir} && find * -type d -exec echo '-mkdir {}' \; >> ${temp_script}
	cd ${temp_dir} && find * -type f -exec echo 'put {} {}' \; >> ${temp_script}
	sftp -b ${temp_script} jross@home.apache.org:public_html/pumpjack
	rm -rf ${temp_dir}
	rm ${temp_script}

.PHONY: update-markdown2
update-markdown2:
	curl "https://raw.githubusercontent.com/ssorj/transom/master/python/markdown2.py" -o python/markdown2.py

.PHONY: update-pencil
update-pencil:
	curl "https://raw.githubusercontent.com/ssorj/pencil/master/python/pencil.py" -o python/pencil.py
