# Flujo Apio para Nexys4 DDR / Nexys A7-100T.
# Uso:
#   make convert TOP=mi_diseno.py
#   make build   TOP=mi_diseno.py   # tambien acepta .v
#   make upload  TOP=mi_diseno.py   # tambien acepta .v
#   make clean
#
# Con TOP=.py, build/upload ejecutan convert automaticamente.

TOP ?= bcd_counter_8digit.py

.DEFAULT_GOAL := build

ifeq ($(suffix $(TOP)),.py)
  TOP_V      := $(TOP:.py=.v)
  BUILD_DEPS := convert
else
  TOP_V      := $(TOP)
endif

TOP_NAME := $(basename $(notdir $(TOP_V)))
XDC      := $(basename $(TOP_V)).xdc

APIO_INI = printf '%s\n' '[env:build]' 'board = nexys-a7-100t' 'top-module = $(TOP_NAME)' 'constraint-file = $(XDC)' 'nextpnr-extra-options =' '    --freq 100' > apio.ini

.PHONY: convert build upload clean

convert:
	@case "$(TOP)" in \
	  *.py) cd "$(dir $(TOP))" && python3 "$(notdir $(TOP))";; \
	  *) echo "ERROR: convert requiere TOP=archivo.py"; exit 1;; \
	esac
	@$(APIO_INI)

build: $(BUILD_DEPS)
	@$(APIO_INI)
	apio build

upload: $(BUILD_DEPS)
	@$(APIO_INI)
	apio upload

clean:
	-apio clean
	rm -f apio.ini
	rm -f "$(TOP_V)"
	rm -rf _build __pycache__
