include contrib/*.mk

.PHONY: 1-new-draft
## Create a new draft in the _drafts folder
1-new-draft:
	@bash contrib/new-draft.sh


.PHONY: 2-start-server
## Start a Jekyll server at port 4000
2-start-server:
	@@UID=$$(id -u) GID=$$(id -g) docker compose -f contrib/docker-compose.yml up jekyll_site

.PHONY: 3-stop-server
## Close the jekyll server
3-stop-server:
	@docker compose -f contrib/docker-compose.yml down

.PHONY: 4-push-source
## Push to source branch
4-push-source:
	@bash contrib/push-source.sh



.PHONY: clean
# Remove _site, .jekyll-cache i .jekyll-metadata
clean:
	@sudo rm -rf _site .jekyll-cache .jekyll-metadata


