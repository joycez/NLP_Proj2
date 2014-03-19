from sup_preprocessing import *
from sup_model import *
from inference import *
from nltk import *

def main():
##        fM1 = featureModel('training_data.data',3)
  fM1 = featureModel('sample.data',3)
  print fM1.probSense('exchange.n','5')
        # print fM1.probFeature('area.n','2','superiority')
##  evaluateValidFile('validation_data.data')
               
if __name__ == "__main__":
  main()
