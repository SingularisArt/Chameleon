PREFIX = ~/.local
CONFIG = ~/.config
PIPVER = `command -v pip3 || command -v pip`
CONF_FILE = $(XDG_CONFIG_HOME)/hue/config.yaml
CURRENT_DIR = $(PWD)

install:
	mkdir -p $(PREFIX)/bin
	cp -f hue.py $(PREFIX)/bin/hue
	@echo "hue.py has been installed to $(PREFIX)/bin/hue"
	mkdir -p $(CONFIG)/hue
	-mv $(CONF_FILE) $(CONF_FILE)-backup 2>/dev/null
	-cp -r $(CURRENT_DIR)/config-template.yaml $(CONF_FILE)
	@echo "installing $(PIPVER) dependencies"
	@$(PIPVER) install whichcraft || echo "dependencies couldn't be installed install pip and rerun"
	@$(PIPVER) install pywal || echo "dependencies couldn't be installed install pip and rerun"
uninstall:
	-rm -rf $(CONFIG)/hue
	@echo "removed $(CONFIG)/hue"
