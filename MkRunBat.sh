#!/bin/sh

################################################################
#-----------------------C A U T I O N S------------------------#
################################################################
#                                                              #
# 0. bash shell script to make batch jobs & cfg python scripts #
# 1. frontpath & storage have to end with /                    #
# 2. cfgpy & batch (test.py & mjob.csh) must be placed         #
#    in the same directory with this script                    #
# 3. Before you really submit the jobs, please open and check  #
#    the contents of .py & .csh                                #
#                                                              #
################################################################

#------------------- Set up the paramters ---------------------#
input=list  # list of input files [example : nsls cms370/EmbMuSkim2 >& list]
bunch=50   # the number of input files to be putted in the 1 cfg .py file
frontpath=/castor/cern.ch/cms/store/relval/CMSSW_3_9_0_pre5/RelValHydjetQ_MinBias_2760GeV/GEN-SIM-DIGI-RAW-HLTDEBUG/MC_39Y_V0-v1/0028/ # root path for input files
storage=/castor/cern.ch/user/m/miheejo/cms390p5/HIDQM_HYD/  # final storage directory
output=step2_recodqm_   # name of output file
jname=DQMstep2_          # name of the batch jobs
cfgpy=step2_MC1_2_RAW2DIGI_RECO_DQM.py           # name of skeleton cfg .py
batch=mjob.csh          # name of skeleton batch job script (.sh/.csh)
#--------------------------------------------------------------#

# Making the input bunchs
echo Reading data directory now ...
rfdir $frontpath > $input
#awk -v p='"rfio:'$frontpath '{if($5 > 130000000) print p$9"\","}' $input > tmp.txt
awk -v p='"rfio:'$frontpath '{print p$9"\","}' $input > tmp.txt

exec 4<&0   #Save stdin
#exec 7>&1   #Save stdout

#----------------- File processing parameters -----------------#
i=1           # number of lines in the input file (Do not edit)
j=1           # output file number starts from this
startline=1   # read 'tmp.txt' from this line
nfiles=-1     # total number of produced .py .csh files (-1 for all)
#--------------------------------------------------------------#

#-------------------- Temporary variables ---------------------#
totfile=$(expr $j + $nfiles)
tmp=""
#--------------------------------------------------------------#

# Making .py .csh files
exec < tmp.txt
while read line
do
    if [ $i -lt $startline ]        # Start at the middle of '$file'
    then
      i=$(expr $i + 1);
      continue;
    fi
    if [ $nfiles -ne -1 ]           # nfiles == -1 : produce all .py .csh
    then
      if [ $j -eq $totfile ]        # Limit number of total production of .py .csh
      then
        break;
      fi
    fi
    
    tmp=$tmp$line;
    if [ $i -eq $(wc -l <$input) ]   # To make the last .py
    then
        awk -v p=$tmp -v p2=\"$output$j.root\" '{gsub("_input_",p); gsub("_output_",p2); print;}' $cfgpy > $jname$j.py;
        awk -v p=$(pwd) -v p2=$jname$j.py -v p3=$output$j.root -v p4=$storage '{gsub("_pwd_",p); gsub("_input_py_",p2); gsub("_output_file_",p3); gsub("_storage_",p4); print;}' $batch > $jname$j.csh;
        echo $jname$j.py $jname$j.csh;
        #bsub -R "pool>10000" -q 1nd -J $jname$j < $jname$j.csh
    elif [ $(($i%$bunch)) -eq 0 ]   # Complete input file for 1 .py
    then 
        awk -v p=$tmp -v p2=\"$output$j.root\" '{gsub("_input_",p); gsub("_output_",p2); print;}' $cfgpy > $jname$j.py;
        awk -v p=$(pwd) -v p2=$jname$j.py -v p3=$output$j.root -v p4=$storage '{gsub("_pwd_",p); gsub("_input_py_",p2); gsub("_output_file_",p3); gsub("_storage_",p4); print;}' $batch > $jname$j.csh;
        echo $jname$j.py $jname$j.csh;
        #bsub -R "pool>10000" -q 1nd -J $jname$j < $jname$j.csh
        tmp="";
        j=$(expr $j + 1);
    fi
    i=$(expr $i + 1);              # Count the line number in the tmp.txt
done

#exec 1>&7 7>&-   #Restore stdout & close fd 7
exec 0<&4 4<&-   #Restore stdin & close fd 4

rm -f tmp.txt
