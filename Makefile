.PHONY: help generate clean publish update-pencil

tmpdir := $(shell mktemp -d)
pygments_style := monokai

generate: clean
	PYTHONPATH=${PWD}/python scripts/pumpjack -r html -i proton -o input
	transom input output --site-url "file://${PWD}/output"

help:
	@echo "generate, clean, publish"

clean:
	find python -type f -name \*.pyc -delete
	rm -rf output

publish: temp_dir := $(shell mktemp -d)
publish:
	chmod 755 ${temp_dir}
	transom input ${temp_dir} --site-url "/~jross/pumpjack"
	rsync -av ${temp_dir}/ jross@people.apache.org:public_html/pumpjack
	rm -rf ${temp_dir}

update-pencil:
	curl "https://raw.githubusercontent.com/ssorj/pencil/master/python/pencil.py" -o python/pencil.py
