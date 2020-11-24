-include horizon/.hzn.json.tmp.mk
export ARCH ?= $(shell hzn architecture)

publish-service:
	hzn exchange service publish -O -f horizon/service.definition.json --pull-image

horizon/.hzn.json.tmp.mk: horizon/hzn.json
	@ hzn util configconv -f $< | sed 's/=/?=/' > $@