-include horizon/.hzn.json.tmp.mk
export ARCH ?= $(shell hzn architecture)

build:
	docker build -t $(DOCKER_IMAGE_BASE):$(SERVICE_VERSION) -f ./Dockerfile.$(ARCH) .

publish-service:
	hzn exchange service publish -O -f horizon/service.definition.json

publish-service-policy:
	hzn exchange service addpolicy -f horizon/service.policy.json $(HZN_ORG_ID)/$(SERVICE_NAME)_$(SERVICE_VERSION)_$(ARCH)

publish-deployment-policy:
	hzn exchange deployment addpolicy -f horizon/deployment.policy.json $(HZN_ORG_ID)/policy-$(SERVICE_NAME)_$(SERVICE_VERSION)_$(ARCH)

build-publish-all-arches:
	$(MAKE) build
	$(MAKE) publish-service
	$(MAKE) publish-service-policy
	$(MAKE) publish-deployment-policy

horizon/.hzn.json.tmp.mk: horizon/hzn.json
	@ hzn util configconv -f $< | sed 's/=/?=/' > $@
