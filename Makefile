include contrib/*.mk

.PHONY: 1-new-draft
## Create a new draft in the _drafts folder
1-new-draft:
	@bash contrib/new-draft.sh


.PHONY: 2-start-server
## Start a Jekyll server at port 4000
2-start-server:
	@docker compose -f contrib/docker-compose.yml up jekyll_site

.PHONY: 3-stop-server
## Close the jekyll server
3-stop-server:
	@docker compose -f contrib/docker-compose.yml down

.PHONY: 4-push-source
## Push to source branch
4-push-source:
	@bash contrib/push-source.sh



.PHONY: clean super-clean
clean:
	@bundle exec jekyll clean   # elimina _site, .jekyll-cache i .jekyll-metadata

super-clean:
	@bundle exec jekyll clean
	@rm -rf vendor/bundle


standarize-images:
	@rename 'y/A-Z/a-z/' images/*
	@rename 'y/\_/-/' images/*
