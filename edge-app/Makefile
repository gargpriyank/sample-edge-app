-include horizon/.hzn.json.tmp.mk
export ARCH ?= $(shell hzn architecture)

build:
	docker build -t $(DOCKER_IMAGE_BASE):$(SERVICE_VERSION) -f ./Dockerfile.$(ARCH) .

build-all-arches:
	ARCH=amd64 $(MAKE) build
	ARCH=arm $(MAKE) build
	ARCH=arm64 $(MAKE) build

publish-service:
	hzn exchange service publish -O -f horizon/service.definition.json

publish-service-policy:
	hzn exchange service addpolicy -f horizon/service.policy.json $(HZN_ORG_ID)/$(SERVICE_NAME)_$(SERVICE_VERSION)_$(ARCH)

publish-deployment-policy:
	hzn exchange deployment addpolicy -f horizon/deployment.policy.json $(HZN_ORG_ID)/policy-$(SERVICE_NAME)_$(SERVICE_VERSION)_$(ARCH)

build-publish-all-arches:
	$(MAKE) build-all-arches
	ARCH=amd64 $(MAKE) publish-service
	ARCH=amd64 $(MAKE) publish-service-policy
	ARCH=amd64 $(MAKE) publish-deployment-policy
	ARCH=arm $(MAKE) publish-service
	ARCH=arm $(MAKE) publish-service-policy
	ARCH=arm $(MAKE) publish-deployment-policy
	ARCH=arm64 $(MAKE) publish-service
	ARCH=arm64 $(MAKE) publish-service-policy
	ARCH=arm64 $(MAKE) publish-deployment-policy

horizon/.hzn.json.tmp.mk: horizon/hzn.json
	@ hzn util configconv -f $< | sed 's/=/?=/' > $@