all: gen.py g_test.txt
	python3 gen.py g_test.txt
	gcc parser.c -o parser

gen:
	python3 gen.py $(in)
	gcc parser.c -o $(out)

clean:
	rm *.c
	rm *.h
