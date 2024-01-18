CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

install:
	@read -p "We need to add aliases. Path to your shell .rc: " SP
	@echo 'alias sitemanager="python3.11 $(CWD)/main.py"' >> SP
