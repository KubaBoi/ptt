import inspect

class M:
	MAKE_FILE_TEMP = """
# MAKEFILE GENERATED BY PTT
# https://github.com/KubaBoi/ptt

NAME=$NAME$
OBJFILES=$(NAME).o $MODULES$

CC=$COMPILER$
CFLAGS= $COMPILER_ARGS$

%.o : %.c 
	$(CC) $(CFLAGS) -c $<

all: $(NAME)

dep:
	$(CC) -MM *.c >dep.list

-include dep.list

$(NAME): $(OBJFILES)
	$(CC) $(CFLAGS) $(OBJFILES) -o $@
	"""

class V:
	VERSION = "1.0.13"

class C:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	
	SILENT = False
	MILLI_SECONDS = False
	RAW = False
	TESTS = True
	FFLUSH = True
	# 0 - C
	# 1 - ASSEMBLER
	MODE = 0 
	POST_FIX = ".c"
	
	@staticmethod
	def noColors():
		members = inspect.getmembers(C, lambda a:not(inspect.isroutine(a)))
		for i in members:
			if (i[0][0] != "_"): setattr(C, i[0], "")
			
	@staticmethod
	def silent():
		C.SILENT = True
		
	@staticmethod
	def milliseconds():
		C.MILLI_SECONDS = True

	@staticmethod
	def raw():
		C.RAW = True

	@staticmethod
	def tests():
		C.TESTS = False
			
	@staticmethod
	def prnt(*str):
		if (not C.SILENT): print(*str)

	@staticmethod
	def fflush():
		C.FFLUSH = False

	@staticmethod
	def assembler():
		C.MODE = 1
		C.POST_FIX = ".s"
		C.fflush()