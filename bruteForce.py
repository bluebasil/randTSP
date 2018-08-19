import subprocess
import string
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('inputFile',
#                   help='the Suduku file to import.  Should be 9 rows, 9 colums each seperated by spaces.  0 represents a blank space.')
#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--result', action="store_true",
                   help='outputs results instead of average times')

args = parser.parse_args()


programs = ['.\A1Q1Againy.py']#,'solution.py']#['.\A1Q2A.py','.\A1Q2B.py','.\A1Q2C.py']
difficulties = 16
test = 10
tag = "-n"
if args.result:
	tag = "-r"
for path in programs:
	print(path)
	for d in range(1,difficulties + 1):
		total = 0
		count = 0
		for t in range(1, test + 1):
			probPath = ".\\randTSP\\" + str(d) + "\\instance_" + str(t) + ".txt"
			#print(probPath)
			result = subprocess.run(['python', path, probPath, tag], stdout=subprocess.PIPE)
			if len(str(result.stdout)) > 18:
				print(str(result.stdout))
				#total += 10000
			else:
				count += 1
				if args.result:
					print(float(((str(result.stdout).split("'"))[1].split("\\"))[0]))
				else:
					#print(str(result.stdout))
					total += float(((str(result.stdout).split("'"))[1].split("\\"))[0])
		if not args.result:
			print(total/count)

#result = subprocess.run(['python.exe', '.\A1Q2A.py', "./problems\\" + str(70) + "\\" + str(1) + ".sd", '-r'], stdout=subprocess.PIPE)

#print(int(((str(result.stdout).split("'"))[1].split("\\"))[0]))
