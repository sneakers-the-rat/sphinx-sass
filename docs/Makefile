SRCDIR=source
BLDDIR=build
EXTENSIONS=
WATCH=-z ../sphinx_sass -z ./$(SRCDIR) $(EXTENSIONS)
CMDOPT=-E -a -d $(BLDDIR)/.doctrees
IGNORE=

clean:
	rm -r $(BLDDIR)

html:
	sphinx-build $(CMDOPT) -b html  $(SRCDIR) $(BLDDIR)

watch:
	sphinx-autobuild $(WATCH) $(IGNORE) $(CMDOPT) -b html  $(SRCDIR) $(BLDDIR)

