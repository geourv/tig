# paths
SRC        ?= assets/logo.svg
DESIGN     ?= docs_quarts_de_docs
ICONS_DIR  ?= assets/icons/$(DESIGN)

.PHONY: icons icons-pwa icons-ico icons-og icons-clean
## Generate minimal, modern logo set (SVG + 32px PNG + apple-touch 180). Extra: --ico / --pwa / --og banner
icons:
	@chmod +x contrib/make-logos.sh
	@contrib/make-logos.sh "$(SRC)" "$(ICONS_DIR)"
	@echo "icons written to: $(ICONS_DIR)"

icons-pwa:
	@chmod +x contrib/make-logos.sh
	@contrib/make-logos.sh "$(SRC)" "$(ICONS_DIR)" --pwa
	@echo "icons (PWA) written to: $(ICONS_DIR)"

icons-ico:
	@chmod +x contrib/make-logos.sh
	@contrib/make-logos.sh "$(SRC)" "$(ICONS_DIR)" --ico
	@echo "favicon.ico added in: $(ICONS_DIR)"

OG_BANNER ?= assets/og-banner.svg
icons-og:
	@chmod +x contrib/make-logos.sh
	@contrib/make-logos.sh "$(SRC)" "$(ICONS_DIR)" --og "$(OG_BANNER)"
	@echo "og image written to: $(ICONS_DIR)/og-1200x630.png"

## Clean/remove all generated icons
icons-clean:
	@rm -rf "$(ICONS_DIR)"
