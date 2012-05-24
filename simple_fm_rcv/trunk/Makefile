TARFILES=simple_fm_rcv.py simple_fm_rcv.grc handle_rds.c simple_fm_helper.py simple_fm_rcv Makefile
handle_rds: handle_rds.o
install: handle_rds simple_fm_rcv.py
	-mkdir $(HOME)/bin
	cp -p handle_rds simple_fm_rcv.py simple_fm_rcv simple_fm_helper.py $(HOME)/bin
	
tarfile:
	tar czvf simple_fm_rcv.tar.gz $(TARFILES)
clean:
	\rm -f handle_rds handle_rds.o
