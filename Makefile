all: gen.py g_test.txt
	python3 gen.py g_test.txt
	gcc parser.c -o parser

gen:
	python3 gen.py $(in)
	gcc parser.c -o $(out)

test: test_running_time/test_running_time.py
	python3 test_running_time/test_running_time.py
	

clean:
	rm -f *.c
	rm -f *.h
	rm -f parserToTest
	rm -f test_running_time/*.c
	rm -f test_running_time/*.h
	rm -f test_running_time/parserToTest
