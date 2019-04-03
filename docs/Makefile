SRCDIR=source
BLDDIR=build
DISTDIR=dist
OUTDIR=html
GH_PAGES=$(DISTDIR)/gh-pages
HTMLDIR=$(shell pwd)/$(DISTDIR)/$(OUTDIR)
EXTENSIONS=
WATCH=-z ../sphinx_sass -z ./$(SRCDIR) $(EXTENSIONS)
CMDOPT=-T -d $(BLDDIR)/.doctrees
IGNORE=


html:
	sphinx-build $(CMDOPT) -b html  $(SRCDIR) $(BLDDIR)/html

watch:
	sphinx-autobuild $(WATCH) $(IGNORE) $(CMDOPT) -b html  $(SRCDIR) $(BLDDIR)/$(OUTDIR)

dist: clean-dist
	sphinx-build -E -a -d $(DISTDIR)/.doctrees -b html $(SRCDIR) $(DISTDIR)/$(OUTDIR)

gh-pages: dist
	@mkdir -p $(GH_PAGES); \
	(	\
		cd $(GH_PAGES); \
		git clone `git config --get remote.origin.url`; \
		cd `ls`; \
		git checkout -B gh-pages; \
		rm -rf `find . | grep -v "^\([.]\+\|[.]/[.]git.*\)$$"`; \
		cp -R "$(HTMLDIR)"/* .; \
		touch .nojekyll; \
		git add . &> /dev/null; \
		git commit -a -m "Update gh-pages" &> /dev/null; \
		git push -f origin gh-pages; \
	); \
	make clean-gh-pages;

clean: clean-build clean-dist

clean-build:
	@if [ -d "$(BLDDIR)" ]; then \
		rm -r $(BLDDIR); \
	fi;

clean-dist:
	@if [ -d "$(DISTDIR)" ]; then \
		chmod -R u+rwx $(DISTDIR); \
		rm -r $(DISTDIR); \
	fi;

clean-gh-pages:
	@if [ -d "$(GH_PAGES)" ]; then \
		chmod -R u+rwx $(GH_PAGES); \
		rm -rf $(GH_PAGES); \
	fi
