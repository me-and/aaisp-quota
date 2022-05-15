.DEFAULT: all
.PHONY: all install

INSTALL = install
DESTDIR = /usr/local/bin

# Nothing to build, this is just in case someone expects a bare `make` or `make
# all` command to be run before `sudo make install`.
all: ;

install: aaisp-quota month-left xyakplot.py
	$(INSTALL) $? $(DESTDIR)
