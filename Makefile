all:
	python gen.py g_test2.txt
	gcc parser.c -o parser
