export PYTHONPATH = ${PWD}/python

.PHONY: default
default: render-mercury render-proton

.PHONY: render-mercury
render-mercury: clean
	scripts/pumpjack -r html -i mercury -o input/mercury
	transom render input/mercury output/mercury

.PHONY: render-proton
render-proton: clean
	scripts/pumpjack -r html -i proton -o input/proton
	transom render input/proton output/proton

.PHONY: render-proton-python
render-proton-python:
	scripts/pumpjack -r python -i proton -o input/proton/python
	transom input/proton output/proton

.PHONY: gen-proton-python-impl
gen-proton-python-impl: impl_dir := python/proton/_qpid_proton_impl
gen-proton-python-impl: temp_dir := $(shell mktemp -d)
gen-proton-python-impl:
	scripts/pumpjack -r python-impl -i proton -o ${temp_dir}/new-impl
	-mv ${impl_dir} ${temp_dir}/old-impl
	mv ${temp_dir}/new-impl/qpid_proton ${impl_dir}

.PHONY: help
help:
	@echo "render, clean, publish"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	rm -rf output

.PHONY: publish
publish: temp_dir := $(shell mktemp -d)
publish: temp_script := $(shell mktemp)
publish: render
	chmod 755 ${temp_dir}
	transom input ${temp_dir} --site-url "/~${USER}/pumpjack"
#	rsync -av ${temp_dir}/ ${USER}@people.apache.org:public_html/pumpjack
#	rsync -av ${temp_dir}/ ${USER}@home.apache.org::public_html/pumpjack
	echo 'lcd ${temp_dir}' >> ${temp_script}
	cd ${temp_dir} && find * -type d -exec echo '-mkdir {}' \; >> ${temp_script}
	cd ${temp_dir} && find * -type f -exec echo 'put {} {}' \; >> ${temp_script}
	sftp -b ${temp_script} ${USER}@home.apache.org:public_html/pumpjack
	rm -rf ${temp_dir}
	rm ${temp_script}

.PHONY: test-python
test-python: render-python
	PN_TRACE_FRM=1 PYTHONPATH=output/python:${PYTHONPATH} scripts/test-python

.PHONY: update-markdown2
update-markdown2:
	curl "https://raw.githubusercontent.com/ssorj/transom/master/python/markdown2.py" -o python/markdown2.py

.PHONY: update-pencil
update-pencil:
	curl "https://raw.githubusercontent.com/ssorj/pencil/master/python/pencil.py" -o python/pencil.py
