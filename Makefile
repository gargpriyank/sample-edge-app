export ARCH ?= $(shell hzn architecture)

publish-esf-ieam:
	cd esf-ieam && $(MAKE) publish-service

publish-edge-app:
	cd edge-app && $(MAKE) build-publish

publish:
	$(MAKE) publish-esf-ieam
	$(MAKE) publish-edge-app

register-node-policy:
	cd edge-app && hzn register --policy=horizon/node_policy.json -s edge-app --serviceorg $HZN_ORG_ID -f userinput.json