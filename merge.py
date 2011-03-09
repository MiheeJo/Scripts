#!/bin/python
import sys,string,re,subprocess

foutput = open("fit_parameters","w")
line = "rap" + "\t" + "cent" + "\t" + "Bfrac" + "\t" + "coefExp" + "\t" + \
"fbkgCtTot" + "\t" + "meanResSigW" + "\t" + "sigmaResSigW" + "\t" + \
"sigmaResSigN" + "\t" + "PromptJ/psi" + "\t" + "PromptJ/psiErr" + "\t" + \
"Non-promptJ/psi" + "\t" + "Non-promptJ/psiErr" + "\t" + "Resolution" + "\t" +\
"ResolutionErr" + "\n"
foutput.write(line)

filels = subprocess.call("ls ./results", shell=True)
filelist = filels.split("\n")
for files in filelist:
  data = []
  fname = files.split("_")
  rap = re.search('[0-9]+-[0-9]+',fname[0]).group()
  cent = re.search('[0-9]+-[0-9]+',fname[1]).group()
  print rap, cent

  finput = open("./results/"+files,'r')
  for line in finput:
    tmp = line.split(" ")
    for i in tmp:
      try:
        data.append( float(i) )
      except:
        continue
#  print data

  line = rap + "\t" + cent + "\t"
  for i in data:
    line = line+str(i)+"\t"
  foutput.write(line)
  line = "\n"
  foutput.write(line)
