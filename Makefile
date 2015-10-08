.PHONY: help generate prepare clean test

tmpdir := $(shell mktemp -d)
pygments_style := monokai

generate:
	scripts/pumpjack -r python -i input/proton -o output/proton
	mv output/proton/module.python output/proton/module.py
	scripts/colorize output/proton/module.py output/proton/module.py.html

prepare: clean
#	mkdir -p output/peer/examples
#	mkdir -p output/peer/resources
#	cp -a input/peer/resources/* output/peer/resources

help:
	@echo "generate, clean, test"

clean:
	find python -type f -name \*.pyc -delete
	rm -rf output

test: generate
	python output/peer/module.py

	javac output/peer/module.java

	echo 'int main(int argc, char ** argv) {}' > ${tmpdir}/test.c
	gcc -std=c99 -pedantic -include output/peer/module.c -o ${tmpdir}/test.o ${tmpdir}/test.c

output/%: input/%
	scripts/pumpjack -r c -i $< -o $@
	scripts/pumpjack -r java -i $< -o $@
	scripts/pumpjack -r python -i $< -o $@
	cp $</module.xml $@/module.xml

	mv output/$*/module.python output/$*/module.py

	scripts/colorize output/$*/module.c output/$*/module.c.html 
	scripts/colorize output/$*/module.java output/$*/module.java.html 
	scripts/colorize output/$*/module.py output/$*/module.py.html 
	scripts/colorize output/$*/module.xml output/$*/module.xml.html

	scripts/pumpjack -r html -i $< -o $@

# output/peer/examples/%: input/peer/examples/%
# 	cp $< $@
# 	pygmentize -l `echo $* | cut -d . -f 2` -f html -O style=${pygments_style} $< >> $@.include
# 	bin/templatize input/peer/templates/example.html $@.include $@.html
# 	rm $@.include

# epydoc: output/peer/module.python
# 	PYTHONPATH=output epydoc --output output/peer/epydoc peer.module
