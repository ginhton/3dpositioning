d=$(shell date +%Y-%m-%d_%H:%M:%S)

rec: server.py
	./server.py 8070 rec

rec190: server.py
	timeout --signal=SIGINT 190s ./server.py 8070 rec

task: server.py
	./server.py 8070 task

tri: server.py
	./server.py 8070 triangulator

WCLSimple: server.py
	./server.py 8070 WCLSimple

show: server.py
	./server.py 8070 show

rssi: server.py
	./server.py 8070 rssi

single: single.py
	python single.py 8070

cli: client.py
	./client.py 8070

stat: statics.py
	./statics.py ../data/expriment7

test: test.py
	python ./test.py

rm-quot: *.txt
	sed -i.bak "s/'/\"/g" *.txt
	rm *.bak

clr:
	rm ./*.txt

archive:
	mkdir $d
	mv ./*.txt $d/
