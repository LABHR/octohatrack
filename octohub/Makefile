progname = octohub
prefix = /usr/local
PATH_BIN = $(prefix)/bin
PATH_INSTALL_LIB = $(prefix)/lib/$(progname)

all: help

# target: help
help:
	@echo '=== Targets:'
	@echo 'install   [ prefix=path/to/usr ] # default: prefix=$(value prefix)'
	@echo 'uninstall [ prefix=path/to/usr ]'
	@echo
	@echo 'clean'

# DRY macros
truepath = $(shell echo $1 | sed -e 's/^debian\/$(progname)//')
libpath = $(call truepath,$(PATH_INSTALL_LIB))/$$(basename $1)
subcommand = $(progname)-$$(echo $1 | sed 's|.*/||; s/^cmd_//; s/_/-/g; s/.py$$//')
echo-do = echo $1; $1

# first argument: code we execute if there is just one executable module
# second argument: code we execute if there is more than on executable module
define with-py-executables
	@modules=$$(find -maxdepth 1 -type f -name '*.py' -perm -100); \
	modules_len=$$(echo $$modules | wc -w); \
	if [ $$modules_len = 1 ]; then \
		module=$$modules; \
		$(call echo-do, $1); \
	elif [ $$modules_len -gt 1 ]; then \
		for module in $$modules; do \
			$(call echo-do, $2); \
		done; \
	fi;
endef

# target: install
install:
	@echo
	@echo \*\* CONFIG: prefix = $(prefix) \*\*
	@echo 

	install -d $(PATH_BIN) $(PATH_INSTALL_LIB)
	python setup.py install --prefix $(prefix) --install-layout=deb
	cp cmd*.py $(PATH_INSTALL_LIB)

	$(call with-py-executables, \
	  ln -fs $(call libpath, $$module) $(PATH_BIN)/$(progname), \
	  ln -fs $(call libpath, $$module) $(PATH_BIN)/$(call subcommand, $$module))

# target: uninstall
uninstall:
	rm -rf $(PATH_INSTALL_LIB)

	$(call with-py-executables, \
	  rm -f $(PATH_BIN)/$(progname), \
	  rm -f $(PATH_BIN)/$(call subcommand, $$module))

# target: clean
clean:
	rm -f *.pyc */*.pyc
	rm -rf build

