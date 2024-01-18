CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))
FILE := $(shell read -p "We need to add alias. Enter absolute path to your .rc file: " enter ; echo $${enter})

install:
	@echo 'alias sitemanager="python3.11 $(CWD)/main.py"' >> "$(FILE)"
