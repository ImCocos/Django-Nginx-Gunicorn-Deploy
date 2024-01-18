CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

install:
	@echo 'alias sitemanager="python3.11 $(CWD)/main.py"' >> /home/$(shell whoami)/.bash_aliases
	@echo 'alias sitemanager="python3.11 $(CWD)/main.py"' >> /home/$(shell whoami)/.zshrc
