FILES = ./mod/AXNODE.mod ./mod/kdr.mod ./mod/Xtra.mod ./mod/nahh.mod

all:
	nrnivmodl $(FILES)

clean:
	rm -rf umac i386 x86_64