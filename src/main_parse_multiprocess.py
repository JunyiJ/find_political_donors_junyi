import heapq
import time
from collections import defaultdict
import sys
from multiprocessing import Process
from os.path import abspath,dirname,join,isdir,isfile
from os import listdir


def get_median_sum(zipDict,CMTE_ID,ZIP_CODE,TA_AMT):
	## update zipDict based on key (CMTE_ID,ZIP_CODE)
	## get running median,number of transactions, amount of transactions for (CMTE_ID,ZIP_CODE)
	## zipDict:[amt,n_transactions,n_minheap,maxheap,minheap]
	## maintain len(maxheap)==len(minheap) or len(maxheap)==len(minheap)+1
	if (CMTE_ID,ZIP_CODE) not in zipDict:
		zipDict[(CMTE_ID,ZIP_CODE)] = [TA_AMT,1,0,[],[]]
		maxheap=zipDict[(CMTE_ID,ZIP_CODE)][3]
		heapq.heappush(maxheap,-TA_AMT)
		return TA_AMT,1,TA_AMT
	else:		
		zipDict[(CMTE_ID,ZIP_CODE)][0] += TA_AMT
		zipDict[(CMTE_ID,ZIP_CODE)][1] += 1
		amt,nt,nmin,maxheap,minheap = zipDict[(CMTE_ID,ZIP_CODE)]
		nmax = nt - nmin - 1
		leftmax = -maxheap[0]
		if TA_AMT>leftmax:
			heapq.heappush(minheap,TA_AMT)
			nmin += 1
			if nmin > nmax:
				minright = heapq.heappop(minheap)
				heapq.heappush(maxheap,-minright)
				nmin -= 1
				nmax += 1
		else:
			heapq.heappush(maxheap,-TA_AMT)
			nmax += 1
			if nmax > nmin+1:
				maxleft=heapq.heappop(maxheap)
				heapq.heappush(minheap,-maxleft)
				nmin += 1
				nmax -= 1
		zipDict[(CMTE_ID,ZIP_CODE)][2]=nmin
		median =  -maxheap[0]
		if not nt%2:
			median = int(round((-maxheap[0] + minheap[0])/2.0))
		return (median,nt,amt)

		
def leapyear(Y):
	#check whether Y is leap year
	if Y%4:
		return False
	if not Y%100:
		if Y%400:
			return False
		return True
	return True

def valid_date(date):
	#check whether a date is valid
	if len(date)!=8:
		return False
	for c in date:
		if not c.isdigit():
			return False
	M,D,Y=map(int,[date[:2],date[2:4],date[4:8]])
	if M > 12 or D > 31 or M == 0 or D == 0:
		return False
	if M == 2:
		if D>29:
			return False
		elif D==29:
			if leapyear(Y):
				return True
			return False			
	elif M not in set([1,3,5,7,8,10,12]) and D==31:
		return False
	return True
	
	
def main_zip(inputpath,zipoutfile):
	zipout,zipDict = [],{}
	if not isfile(inputpath):
		# if file doesn't exit, create two output but do nothing
		with open(zipoutfile,"w+"):
			pass
		with open(dateoutfile,"w+"):
			pass
		return
	with open(inputpath,"r") as f:
		for line in f:
			input = line.split("|")
			ninput = len(input)
			if ninput<15: # invalid line
				continue
			CMTE_ID,ZIP_CODE,TA_DT,TA_AMT,OTHER_ID = input[0],input[10],input[13],input[14],None
			if ninput>=15: 
				OTHER_ID = input[15]
			if OTHER_ID or (not CMTE_ID) or (not TA_AMT):
				continue
			#print CMTE_ID,ZIP_CODE,TA_DT,TA_AMT,OTHER_ID
			if len(ZIP_CODE) >= 5:
				try:
					TA_AMT = int(TA_AMT)
					ZIP_CODE = ZIP_CODE[:5]
					zipmedian,nt,amt = get_median_sum(zipDict,CMTE_ID,ZIP_CODE,TA_AMT)
					zipout.append("|".join([CMTE_ID,ZIP_CODE,str(zipmedian),str(nt),str(amt)]))
				except ValueError:
					print("TRANSACTION_AMOUNT is not a valid number")	
	
	with open(zipoutfile,"w+") as f:
		f.write("\n".join(zipout))

def main_date(inputpath,datefile):
	dateDict=defaultdict(list)
	if not isfile(inputpath):
		# if file doesn't exit, create two output but do nothing
		with open(zipoutfile,"w+"):
			pass
		with open(dateoutfile,"w+"):
			pass
		return
	with open(inputpath,"r") as f:
		for line in f:
			input = line.strip().split("|")
			ninput = len(input)
			if ninput<15: # invalid line
				continue
			CMTE_ID,ZIP_CODE,TA_DT,TA_AMT,OTHER_ID = input[0],input[10],input[13],input[14],None
			if ninput>=15: 
				OTHER_ID = input[15]
			if OTHER_ID or (not CMTE_ID) or (not TA_AMT):
				continue
			if OTHER_ID or (not CMTE_ID) or (not TA_AMT):
				continue
			#print CMTE_ID,ZIP_CODE,TA_DT,TA_AMT,OTHER_ID
			if valid_date(TA_DT):
				try:
					TA_AMT = int(TA_AMT)
					dateDict[(CMTE_ID,TA_DT)].append(TA_AMT)
				except ValueError:
					print("TRANSACTION_AMOUNT is not a valid number")
	
	with open(dateoutfile,"w+") as f:
		for key in sorted(dateDict.keys()):
			dateDict[key].sort()
			CMTE_ID,date = key
			nt = len(dateDict[key])
			total = sum(dateDict[key])
			median = dateDict[key][nt//2]
			if not nt%2:
				median = int(round((dateDict[key][nt//2-1]+dateDict[key][nt//2])/2.0))
			f.write("|".join([CMTE_ID,date,str(median),str(nt),str(total)])+"\n")

# Parse commandline para to get inputpath and outfile names.
if __name__ == "__main__":
	n = len(sys.argv)
	if n == 4:
		# command line specifies the inputfile and outputfiles
		inputpath = sys.argv[1]
		zipoutfile = sys.argv[2]
		dateoutfile = sys.argv[3]
		p1=Process(target=main_zip,args=(inputpath,zipoutfile,))
		p1.start()		
		main_date(inputpath,dateoutfile)
		p1.join()
	else:
		print("Wrong cammand line argument number")




				
				
				


