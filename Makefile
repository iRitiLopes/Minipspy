.DEFAULT_GOAL := build

SOURCE ?= examples/cache_probe.c
BUILD_DIR ?= build/mips
DOCKER ?= 1
IMAGE ?= minipspy-toolchain
CROSS ?= mipsel-linux-gnu-
PYTHON ?= python3
MODE ?= 6
STAT ?= 0
PROGRAM := $(BUILD_DIR)/$(notdir $(basename $(SOURCE)))

.PHONY: build toolchain run check help

ifeq ($(DOCKER),1)
build:
	docker image inspect "$(IMAGE)" >/dev/null 2>&1 || \
	    docker build -t "$(IMAGE)" -f tools/Dockerfile.mips .
	docker run --rm --user "$(shell id -u):$(shell id -g)" \
	    -v "$(CURDIR):/work" "$(IMAGE)" \
	    make -f tools/Makefile.mips SOURCE="$(SOURCE)" BUILD_DIR="$(BUILD_DIR)" CROSS="$(CROSS)"
else
build:
	$(MAKE) -f tools/Makefile.mips SOURCE="$(SOURCE)" BUILD_DIR="$(BUILD_DIR)" CROSS="$(CROSS)"
endif

toolchain:
	docker build -t "$(IMAGE)" -f tools/Dockerfile.mips .

run: build
	$(PYTHON) main.py run "$(MODE)" "$(PROGRAM)" $(if $(filter 1,$(STAT)),--stat)

check: build
	$(PYTHON) tools/check_examples.py "$(PROGRAM)"

help:
	@echo 'make build SOURCE=examples/my_test.c     Compile C or C++ using Docker (default)'
	@echo 'make build SOURCE=examples/my_test.cpp   Compile C++'
	@echo 'make build DOCKER=0 SOURCE=examples/my_test.c   Use a locally installed cross-compiler'
	@echo 'make run SOURCE=examples/my_test.c MODE=6      Build and run'
	@echo 'make run SOURCE=examples/my_test.c STAT=1      Include execution statistics'
	@echo 'make check SOURCE=examples/my_test.c     Build and compare all six memory modes'
	@echo 'make toolchain                          Build or update the Docker compiler image'
