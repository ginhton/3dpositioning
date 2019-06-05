d=$(shell date +%Y-%m-%d_%H:%M:%S)

rec: server.py
	./server.py 8070 rec

anl: server.py
	./server.py 8070 realtime

show: server.py
	./server.py 8070 show


cli: client.py
	./client.py 8070

clr:
	rm ./*.txt

archive:
	mkdir $d
	mv ./*.txt $d/
