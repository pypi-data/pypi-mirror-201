"""
    functions_tex.py

    extracts tex environment from a tex file

"""

def create_files(filepath, n, nf, extension):
	"""
	This function takes four inputs and returns tex filenames with proper path 
	
	    filepath -> path to be modified with filename
	    n -> nth of files to be produced
	    nf -> number of files to be produced
        extension -> file extension
	
	    Eg: filepath = "./test/main.tex" -> "./test/main-0.tex, main-1.tex" like that
	"""
	path = filepath.split('.')
	pathinit = filepath.split('/')
	if nf == 1:
	    if pathinit[0] == '.':
	        return '.' + path[len(path)-2] + '.' + extension
	    else:
	        return path[len(path)-2] + '.' + extension
	else:
	    if pathinit[0] == '.':
	        return '.' + path[len(path)-2] + '-' + str(n + 1) +  '.' + extension
	    else:
	        return path[len(path)-2] + '-' + str(n + 1) + '.' + extension
	




files = []


def extract_tex_env(inputfile, outputfile, environment):
    start = []
    end = []
    ntikz = []

    with open(inputfile, 'r') as tex:
        for (n, line) in enumerate(tex):
            if line.strip() == ("\\begin{" + environment + "}"):
                start.append(n)
                ntikz.append(n)
            if line.strip() == "\\end{" + environment + "}":
                end.append(n)
    print(len(ntikz))
    for i in range(len(ntikz)):
        if len(ntikz) == 1:
            outputtex = open(create_files(outputfile, i, len(ntikz), "tex"), 'w')
            files.append(create_files(outputfile, i, len(ntikz), "tex"))
            with open(inputfile, 'r') as tex:
                for (n, line) in enumerate(tex):
                    if n >= start[i] and n <= end[i]:
                        print(line)
                        outputtex.write(line)
        else:
            outputtex = open(create_files(outputfile, i, len(ntikz), "tex"), 'w')
            files.append(create_files(outputfile, i, len(ntikz), "tex"))
            with open(inputfile, 'r') as tex:
                for (n, line) in enumerate(tex):
                    if n >= start[i] and n <= end[i]:
                        print(line)
                        outputtex.write(line)


