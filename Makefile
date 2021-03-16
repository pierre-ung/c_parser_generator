all:
	python gen.py g_test.txt
	gcc parser.c -o parser
