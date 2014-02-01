# Makefile for MSc Dissertation
# Nuno Carvalho -- based on Andreas Linz's
# http://tex.stackexchange.com/a/122263
#
# @ supresses command output
#
# conditionals are not allowed to have a starting tab, 
# otherwise they will be sent to the shell
#
# Set this option to false if you wish not to use a BUILD_DIR folder to
# compilation, true otherwise
USE_HIDDEN_BUILD=false
LANG=en_US
# use UM cover
TEX=xelatex
# use my cover, and no beautiful fonts :(
#TEX=pdflatex
BIB=biber
BUILD_DIR=.build
OUTPUT_DIR=.
RSYNC_OPTS=--verbose --checksum --recursive --human-readable --progress --exclude=.build \
					 --exclude=.git --exclude=.gitignore --exclude=*.tex.latexmain

# if using hidden build dir, copy tex files to build, and then compile
ifeq ($(USE_HIDDEN_BUILD), true)
pdf: copy_sources compile copy_output
# if not using hidden build dir, compile right here
else
pdf: compile
endif

copy_sources:
	@echo "Copying sources to build folder: $(BUILD_DIR)"
	@rsync $(RSYNC_OPTS) . $(BUILD_DIR)

compile: *.tex *.bib
ifeq ($(USE_HIDDEN_BUILD), true)
	cd $(BUILD_DIR) ;\
	echo -e "\n---------- $(TEX) ---------\n" ;\
	$(TEX) Thesis.tex ;\
	echo -e "\n---------- makeindex ---------\n" ;\
	makeindex Thesis.nlo -s nomencl.ist -o Thesis.nls ;\
	echo -e "\n---------- $(BIB) ---------\n" ;\
	$(BIB) Thesis ;\
	echo -e "\n---------- $(TEX) ---------\n" ;\
	$(TEX) Thesis.tex | grep --ignore-case --extended-regex \
			"info|warning|error|^\([A-Za-z0-9]*\)"
else
	echo -e "\n---------- $(TEX) ---------\n" ;\
	$(TEX) Thesis.tex ;\
	echo -e "\n---------- makeindex ---------\n" ;\
	makeindex Thesis.nlo -s nomencl.ist -o Thesis.nls ;\
	echo -e "\n---------- $(BIB) ---------\n" ;\
	$(BIB) Thesis ;\
	echo -e "\n---------- $(TEX) ---------\n" ;\
	$(TEX) Thesis.tex | grep --ignore-case --extended-regex \
			"info|warning|error|^\([A-Za-z0-9]*\)"
endif

copy_output:
	@echo "Copying generated output to: $(OUTPUT_DIR)"
	@cp -vf $(BUILD_DIR)/*.pdf $(OUTPUT_DIR)

# run aspell on all tex files

aspell:
	for i in `find . -iname "*.tex" -not -path "./$(BUILD_DIR)/*"` ; do \
		aspell -t --dont-tex-check-comments --encoding=utf-8 --lang=$(LANG) check $$i; \
	done

clean:
ifeq ($(USE_HIDDEN_BUILD), true)
	@echo "Cleaning $(BUILD_DIR) folder.."
	@rm -rf $(BUILD_DIR)
else
	@echo "Cleaning folder.."
	@rm -rf *.{aux,bak,bbl,bcf,blg,glo,ilg,lof,log,lot,nlo,nls,out,run*,tdo,toc}
endif

