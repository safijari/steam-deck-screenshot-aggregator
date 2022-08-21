all: check-env
	rsync sdsa.py deck@"$(ip)":/tmp
check-env:
ifndef ip
	$(error ip is undefined)
endif