from sup_preprocessing import *
from sup_model import *
from inference import *
from nltk import *

def main():
	#for i in range(11):
	#	print "Window Size ",i
		evaluateValidFile('validation_data.data', 2)

if __name__ == "__main__":
	main()
