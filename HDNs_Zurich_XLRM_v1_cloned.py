import os
import os.path
import random
from operator import add
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import shutil
import ema_workbench
import time


## Step 2: Function for initiating the main dictionary of climate stations
def create_dic(a):
    '''Function: creating a dictionary for each climate station'''
    
    a = {}
    keys = ['DayTmin', 'TempTmax', 'TempTmin', 'DayTmax', 'Tmax_weight', 'Tmin_weight', 'elev', 'lat', 'long', 'fileName']

    a = {key: None for key in keys}
    return a



def initialize_input_dict (mainFolderHDNs):
    ''' This function returns a dictionary , and addresses of all folders'''
    
    
    '''Step 1''' 
    rootFolder = mainFolderHDNs
    inputFolder = os.path.join(rootFolder,'input')
    TmaxFolder = os.path.join(inputFolder, 'Tmax')
    TminFolder = os.path.join(inputFolder, 'Tmin')
    climate_ref_Folder = os.path.join(inputFolder, 'Climate_ref')
    climate_Ref_Folder_org = os.path.join(inputFolder, 'Climate_ref_no_randomness_0')
    climate_ref_Folder_rand_1 = os.path.join(inputFolder, 'Climate_ref_randomness_1')
    climate_ref_Folder_rand_2 = os.path.join(inputFolder, 'Climate_ref_randomness_2')

    '''Step 2: Reading all files' names inside the Tamx, Tmin, and climate folders'''  
    TmaxFiles = []
    for filename in os.walk(TmaxFolder):
        TmaxFiles = filename[2]
    
    TminFiles = list()
    for filename in os.walk(TminFolder):
        TminFiles = filename[2]

    climate_ref_Files = list()
    for filename in os.walk(climate_ref_Folder):
       climate_ref_Files = filename[2]
    
    '''Step 3: Reading files inside Tmax folder '''
    os.chdir(TmaxFolder)
    with open(TmaxFiles[0], 'r') as file:
        weights_Inputs = file.read()
    with open(TmaxFiles[1], 'r') as file:
        day_Tmax = file.read()
    with open(TmaxFiles[2], 'r') as file:
        x1TmaxThershold = file.read()

    '''Step 4: Reading the lines of files inside Tmax folder'''
    weights_Inputs = weights_Inputs.replace('\n', '\t')
    weights_Inputs = weights_Inputs.split('\t')
    day_Tmax = day_Tmax.replace('\n', '\t').split('\t')
    x1TmaxThershold = x1TmaxThershold.replace('\n', '\t').split('\t')


    '''Step 5: Reading files and lines of files inside Tmin folder''' 
    os.chdir(TminFolder)
    
    with open(TminFiles[0], 'r') as file:
        day_Tmin = file.read()
    with open(TminFiles[1], 'r') as file:
        x2TminThershold = file.read()
    
    day_Tmin = day_Tmin.replace('\n', '\t')
    day_Tmin = day_Tmin.split('\t')
    x2TminThershold = x2TminThershold.replace('\n', '\t').split('\t')


    '''Step 6: Reading the lines of files inside climate folder''' 
    os.chdir(climate_ref_Folder)
    
    with open('pcp.txt', 'r') as file:
        pcpData = file.read()
    with open('tmp.txt', 'r') as file:
        tmpData = file.read()
        
    pcpData = pcpData.split('\n')
    
    for i in range(len(pcpData)):
        pcpData[i] = pcpData[i].split(',')
    
    ## 20210222 Saeid New HDNs
    #for i in range(len(tmpData)):
    #    tmpData[i] = tmpData[i].split(',')

    
    '''Step 7: Initialazing the input dictionary of climate stations which holds the information of accumulation
     and ablation, and etc of the stations''' 
    nameStn = []
    for file in climate_ref_Files:
        if 'p.csv' in file:
            #nameStn.append('n_' + file[-25: -5])
            nameStn.append(file[-25: -5])

    stnDicts = []
    for i in range(len(nameStn)):
        stnDicts.append(create_dic(nameStn[i]))
    
    
    '''Step 8: Assigning the file names to the dictionary'''
    for i in range (len(nameStn)):
        stnDicts[i]['fileName'] = nameStn[i]

    
    '''Step 9: Assigning the Tamx and Tmin values'''
    for stnDict in stnDicts:
        for i, element in enumerate(day_Tmin):
            if element == stnDict['fileName'][:]:
            #if element == stnDict['fileName'][2:]:
                stnDict['DayTmin'] = day_Tmin[i+1]
                
        for i, element in enumerate(x1TmaxThershold):
            if element == stnDict['fileName'][:]:
            #if element == stnDict['fileName'][2:]:
                stnDict['TempTmax'] = x1TmaxThershold[i+1]

        for i, element in enumerate(x2TminThershold):
            if element == stnDict['fileName'][:]:
            #if element == stnDict['fileName'][2:]:  
                stnDict['TempTmin'] = x2TminThershold[i+1]

        for i, element in enumerate(day_Tmax):
            if element == stnDict['fileName'][:]:
            #if element == stnDict['fileName'][2:]:
                stnDict['DayTmax'] = day_Tmax[i+1]

        for i, element in enumerate(weights_Inputs):
            stnDict['Tmax_weight'] = weights_Inputs[1]
            stnDict['Tmin_weight'] = weights_Inputs[3]
            
    '''Step 10: Assigning the elevation, Lat and long to the dictionaries'''
    for i in range(len(stnDicts)):
        for j in range(1, len(pcpData)):
            
            #if pcpData[j][1][2:-1] == stnDicts[i]['fileName'][2:]:
            if pcpData[j][1][:-1] == stnDicts[i]['fileName'][:]:
                stnDicts[i]['lat']= pcpData[j][2]
                stnDicts[i]['long']= pcpData[j][3]
                stnDicts[i]['elev']= pcpData[j][4]
                
    return stnDicts, inputFolder, TmaxFolder, TminFolder, climate_ref_Folder, climate_Ref_Folder_org, \
climate_ref_Folder_rand_1, climate_ref_Folder_rand_2


# Step 3 HDNs Model 
## S3.1 Initializiing the main dictionary for a case study
caseStudyStns = {}
inputFolder = ''
TmaxFolder = ''
TminFolder = ''
climateFolder = ''
climateFolder_org = ''
climateFolder1 = ''
climateFolder2 = ''


root = r'C:\Saeid\Prj100\SA_11_HDNS\case1_Zurich\setup1'
#root = r'C:\Saeid\Prj100\SA_11_HDNS\case2_Basel\setup1'


## calling the function with multiple return values
caseStudyStns, inputFolder, TmaxFolder, TminFolder, climateFolder, climateFolder_org, \
climateFolder1, climateFolder2 = initialize_input_dict(root)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

## 1st column as index: makaing date from 01 01 1981 to 2099 12 31
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date ).days + 1)):
        yield start_date + timedelta(n)


### OR Let's make this function in a more OOP way: SHould be changed to POlicy Health 
class Policy_Health:
#class Policy_Ski:
    def __init__(self, x1TmaxThershold, x2TminThershold):
        self.x1TmaxThershold = x1TmaxThershold
        self.x2TminThershold = x2TminThershold

        
    def policy_release2(self):
        return(self.x1TmaxThershold, self.x2TminThershold)
    
    def policy_release3(self):
        ''' this function should make a matrix of evaluation fot the condition of 100 day ay minimum condition'''
        pass

#class Economic_Model_HDNs:
class Economic_Model_Ski:
    def __init__(self, xCostDay, xRevenueDay):
        self.costDayFixed = xCostDay
        self.revenueDayFixed = xRevenueDay
        
    def economic_costDay(self):
        return(self.costDayFixed)
    
    def economic_revenueDay(self):
        return(self.revenueDayFixed)

class RCP_Model:
    def __init__(self, xRCP, xClimateModel):
        self.input1 = round(xRCP)
        #self.input1 = xRCP
        self.input2 = xClimateModel  
        
    def rcpGenerator(self):
        if self.input1 == 1:
            RCP = str(2.6)
            rcpInt = 1
        if self.input1 == 2:
            RCP = str(4.5)
            rcpInt = 2
        if self.input1 == 3:
            RCP = str(8.5)
            rcpInt = 3
        return(RCP, rcpInt)

    
    def climateModel(self):
        a, b = RCP_Model.rcpGenerator(self)
        
        if b == 1:
            climateModel = round(self.input2*11)
            
        elif b == 2:
            climateModel = 11 + max(1,round(self.input2*25))
            
        else:
            climateModel = 36 + max(1, round(self.input2*31))
            
        return (int(climateModel))

    
def HDNs_Model (xRCP=None, xClimateModel=None, Xfactor1 = None, xCostDay = None, xRevenueDay = None,
                 x1TmaxThershold = None, x2TminThershold = None):

    '''' This function controls the HDNs model in the XLR framework'''
    
    ''' VERY IMPORTANT --- Controling the randomness --- VERY IMPORTANT'''
    xClimateRandomness = round(Xfactor1)
    
    if (xClimateRandomness == 1):
        os.chdir(climateFolder_org)
        src = os.getcwd()
        os.chdir(climateFolder)
        dst = os.getcwd()
        #copytree(src, dst)
        print('Original CH2018 is being used')
    elif (xClimateRandomness == 2) :
        os.chdir(climateFolder1)
        src = os.getcwd()
        os.chdir(climateFolder)
        dst = os.getcwd()
        #copytree(src, dst)
        print('Random Climate realization version 1 is being used')
    else:
        os.chdir(climateFolder2)
        src = os.getcwd()
        os.chdir(climateFolder)
        dst = os.getcwd()
        #copytree(src, dst)
        print('Random Climate realization version 2 is being used')

    os.chdir(climateFolder)
    fnames = os.listdir()
    #randomness_pcp_tmp(fnames, Xfactor1)

    print('HDNs_DMDU: Matching the station names values with CSV files!')   
    
    
    '''Matching the station names values in the dictionary of stations with CSV files in Climate folder of the case Study'''
    pcpCaseStudy = []
    tmpCaseStudy = []

    if (xClimateRandomness == 1):
        for i in range(len(caseStudyStns)):
            pcpCaseStudy.append(os.path.join(climateFolder, caseStudyStns[i]['fileName'] + 'p.csv'))
            tmpCaseStudy.append(os.path.join(climateFolder, caseStudyStns[i]['fileName'] + 't.csv'))
    elif (xClimateRandomness == 2) :
        for i in range(len(caseStudyStns)):
            pcpCaseStudy.append(os.path.join(climateFolder1, caseStudyStns[i]['fileName'] + 'p.csv'))
            tmpCaseStudy.append(os.path.join(climateFolder1, caseStudyStns[i]['fileName'] + 't.csv'))
    else:
        for i in range(len(caseStudyStns)):
            pcpCaseStudy.append(os.path.join(climateFolder2, caseStudyStns[i]['fileName'] + 'p.csv'))
            tmpCaseStudy.append(os.path.join(climateFolder2, caseStudyStns[i]['fileName'] + 't.csv'))

    print('HDNs_DMDU: Building a database for each csv file (tmp and pcp)!')
    
    
    '''Step 6: building a database for each precipitation and temperature file in Climate folder and saving them in a list'''
    '''6.1 reading the csv files as databases'''
    dfpcp = [None for _ in range(len(pcpCaseStudy))]
    dftmp = [None for _ in range(len(tmpCaseStudy))]
    for i in range(len(pcpCaseStudy)):
        dfpcp[i] = pd.read_csv(pcpCaseStudy[i])
        dftmp[i] = pd.read_csv(tmpCaseStudy[i])
        
    '''6.2 making a header for output files'''
    dfpcpCol = dfpcp[0].columns
    dftmpCol = dftmp[0].columns
    
    '''6.3 defining the length of simulations and scenarios'''
    scenariosLength = len(dfpcpCol)
    simulationLength = len(dftmp[0][dftmpCol[0]]) - 1
        
    
    '''Reading the beginning and end of the simulation''' 
    start_date = date(1981, 1, 1)
    end_date = date(2099, 12, 31)
    dateList = []
    for single_date in daterange(start_date, end_date):
        dateList.append(single_date.strftime("%m/%d/%Y"))

    seasonList = []
    for n in range (1981, 2100, 1):
        seasonList.append(str(n))
      


    print('HDNs_DMDU: Part 1 Running the model, looking for extreme events and printing the output!')
    '''################################ PART1 ################################'''
    '''Running the model for each climate station:'''

    for k in range(len(caseStudyStns)):
        
        '''making a header for output files'''
        dfpcpCol = dfpcp[k].columns
        dftmpCol = dftmp[k].columns


        

        '''defining the length of simulations and scenarios'''
        #scenariosLength = len(dfpcpCol)
        scenariosLength = 1
        simulationLength = len(dftmp[0][dftmpCol[0]]) - 1


        '''declaring the initial arrays'''
 
        is_extreme_Tmax =  [0 for _ in range(simulationLength)]
        is_extreme_Tmin =  [0 for _ in range(simulationLength)]
        is_extreme_Compound = [0 for _ in range(simulationLength)]
        total = np.zeros([simulationLength, 3*scenariosLength])




        '''RCP and Climate Model Controler'''
        rcp_Model = RCP_Model(xRCP, xClimateModel)
        RCP, intRCP = rcp_Model.rcpGenerator()
        climateModel = rcp_Model.climateModel()



        '''Running the model for each climate scenario:'''
        for j in range(climateModel, climateModel + 1, 1):


            #for j in range(len(dfpcpCol)):
            ## Reading the information and inputs of the first day of simulation
            todayPCP = dfpcp[k][dfpcpCol[j]].iloc[1] if (dfpcp[k][dfpcpCol[j]].iloc[1] != -99) else 0
            todayTMPMAX = round(dftmp[k][dftmpCol[2*j]].iloc[1],2) if(dftmp[k][dftmpCol[2*j]].iloc[1] != -99) else 0
            todayTMPMIN = round(dftmp[k][dftmpCol[2*j+1]].iloc[1],2) if(dftmp[k][dftmpCol[2*j+1]].iloc[1] != -99) else 0
            todayTMPAVE = round((todayTMPMAX+todayTMPMIN)/2,2) if((todayTMPMAX+todayTMPMIN)/2 != -99) else 0

            '''Thershold Temperatures C
            EMA_workbench_controler for the thershold of hott days and hot nights'''

            policyCities = Policy_Health(x1TmaxThershold, x2TminThershold) ## 30 C and 15 C
            x1TmaxThershold, x2TminThershold = policyCities.policy_release2()
            

            
            '''EMA_workbench_controler for the thershold daily fixed revenue and cost expenses'''



            '''Tmax check of the first day:'''
            if (todayTMPMAX) >= x1TmaxThershold:
                is_extreme_Tmax[0] = 1

            else: is_extreme_Tmax[0] = 0


            '''Tmin check of the first day:'''
            if (todayTMPMIN) >= x2TminThershold:
                is_extreme_Tmin[0] = 1

            else: is_extreme_Tmin[0] = 0

            '''Tmax and Tmin compound check of the first day:'''
            if (is_extreme_Tmax[0] == 1) and (is_extreme_Tmin[0] == 1):
                is_extreme_Compound[0] = 1

            else: is_extreme_Compound[0] = 0


            '''storing three values in a list for the first day'''

            
            total[0,0] = round(is_extreme_Tmax[0], 2)
            total[0,1] = round(is_extreme_Tmin[0], 2)
            total[0,2] = round(is_extreme_Compound[0], 2)


            
            '''For the SECOND DAY to the End of Simulation:'''
            i = 0
            for i in range(2, simulationLength, 1):
                '''# precipitation and temperature missing values were handled'''
                todayPCP = dfpcp[k][dfpcpCol[j]].iloc[i] if (dfpcp[k][dfpcpCol[j]].iloc[i] != -99) else 0
                todayTMPMAX = round(dftmp[k][dftmpCol[2*j]].iloc[i],2) if(dftmp[k][dftmpCol[2*j]].iloc[i] != -99) else 0
                todayTMPMIN = round(dftmp[k][dftmpCol[2*j+1]].iloc[i],2) if(dftmp[k][dftmpCol[2*j+1]].iloc[i] != -99) else 0
                todayTMPAVE = round((todayTMPMAX+todayTMPMIN)/2,2) if((todayTMPMAX+todayTMPMIN)/2 != -99) else 0



                if (todayTMPMAX) >= x1TmaxThershold:
                    is_extreme_Tmax[i-1] = 1

                else: is_extreme_Tmax[i-1] = 0


                '''Tmin check of the first day:'''
                if (todayTMPMIN) >= x2TminThershold:
                    is_extreme_Tmin[i-1] = 1

                else: is_extreme_Tmin[i-1] = 0

                '''Tmax and Tmin compound check of the first day:'''
                if (is_extreme_Tmax[i-1] == 1) and (is_extreme_Tmin[i-1] == 1):
                    is_extreme_Compound[i-1] = 1

                else: is_extreme_Compound[i-1] = 0


                total[i,0] = round(is_extreme_Tmax[0], 2)
                total[i,1] = round(is_extreme_Tmin[0], 2)
                total[i,2] = round(is_extreme_Compound[0], 2)


    
        '''Saving the Outputs of total list in a CSV file in a specific path'''

        ## 1st row as the column names:
        
        columnsDF = []
        #columnsDF_aerSnowCheck = []

        
        
        nameHeader = dfpcpCol[climateModel]



        columnsDF.append('is_Tmax_' + nameHeader)
        columnsDF.append('is_Tmin_' + nameHeader)
        columnsDF.append('isTmax_Tmin_' + nameHeader)


        '''Extreme analyses daily'''
        columnsDF0 = ['DATE']
        dfnew0 = pd.DataFrame(dateList, columns = columnsDF0)
        dfnew1 = pd.DataFrame(total, columns = columnsDF)
        df1 = pd.concat([dfnew0, dfnew1], axis=1, sort=False)





        if os.path.isdir(os.path.join(root, 'Outputs_py')):
            pass
        else: os.mkdir(os.path.join(root, 'Outputs_py'))


        '''Make CSvs for daily extreme Outputs'''
        outfolder =os.path.join(root, 'Outputs_py') 
        outfileName = 'Total_daily_' + caseStudyStns[k]['fileName'] + '.csv'
        outputFile = os.path.join(outfolder, outfileName )
        df1.to_csv(outputFile, index = False)


        print('End of Part 1 Calculations!')



        '''################################ PART2 ################################'''
        '''##### PART 2 seasonal outputs Tipping points and Liklihood of Survival#####'''
        
        print('Snow_Model: Starting Part 2, Running the model, seasonal outputs, reading files!')

        #### 20210226 ####
        total_Daily_FilesAll = list()
        total_Daily_Files = []
        
        #### 2020/06/22 ####
        #total_Money_Files = []

        for filename in os.walk(outfolder):
            total_Daily_FilesAll = filename[2]

        
        for bIndex in range (len(total_Daily_FilesAll)):        
            if 'Total_daily_' in total_Daily_FilesAll[bIndex]:
                total_Daily_Files.append(total_Daily_FilesAll[bIndex])


            else: continue
        

        '##Adding the whole address of directory to the name of total daily snow files'''
        totalFiles = []
        for i in range(len(total_Daily_Files)):
            totalFiles.append(os.path.join(outfolder, total_Daily_Files[i])) 

    
        '''##Adding the whole address of directory to the name of total daily money files'''



        print('Snow Model: Continuing of Part 2, Seasonal Outputs, Performing  Tipping Points Analyses!')
        
        
        ## databases are read here: 
        dfSeason = [ None for _ in range(len(totalFiles))]
        
        ##2020/06/22
        #dfSeasonMoney = [ None for _ in range(len(totalMoneyFiles))]



##Here we calcluate seasonal tipping points here
        for i in range(len(totalFiles)):
            dfSeason[i] = pd.read_csv(totalFiles[i], low_memory=False)

            
            start_date = date(1981, 1, 1)
            end_date = date(2099, 12, 31)
            dateList = []
            for single_date in daterange(start_date, end_date):
                dateList.append(single_date.strftime("%m/%d/%Y"))

            start_season = []
            end_season = []

            for pp in range (1981, 2099, 1):
                start_season.append(date(pp, 1, 1))
                end_season.append(date(pp, 12, 31))

            df2 = dfSeason[i]
            df2.set_index('DATE', inplace = True)
            df2Col = df2.columns

            df2ColCal = []
            
            for m in range(1):
            #for m in range(68):
                df2ColCal.append(df2Col[3*m+2])

            sumGoodCondition = np.zeros([len(start_season), len(df2ColCal)])
            #sumRows = np.zeros(len(df2ColCal))  ### Saeed  2020/06/11
            sumRows = np.zeros(len(start_season)) ### Saeed  2020/08/17
 
            for j in range(len(df2ColCal)):
                for k in range(len(start_season)):
                #for i in range(3):
                    start_date = start_season[k]
                    end_date = end_season[k]
                        #start_date = date(1981, 1, 2)
                        #end_date = date(1981, 1, 10)
                    for single_date in daterange(start_date, end_date):
                        sumGoodCondition[k,j] += df2[df2ColCal[j]].loc[single_date.strftime("%m/%d/%Y")]
                    #sumRows[j] +=  sumGoodCondition[k,j] ### Saeed  2020/06/11
                    sumRows[k] +=  sumGoodCondition[k,j]  ### Saeed  2020/08/17
                                                                                                                                                                                                                                                                 

            AveragesumRows = np.average(sumRows) ## Saeed 2020/08/17
            df3 = pd.DataFrame(sumGoodCondition, columns = df2ColCal)


            firstCol = []
            for o in range (len(seasonList)-1):
                #firstCol.append(seasonList[o] +'-' + seasonList[o+1])
                firstCol.append(seasonList[o])


            columnsDF1 = ['Season']
            dfnew3 = pd.DataFrame(firstCol, columns = columnsDF1)

            dfFinalSeason = pd.concat([dfnew3, df3], axis=1, sort=False)          
            
            if os.path.isdir(os.path.join(root, 'outSeason')):
                pass
            else: 
                os.mkdir(os.path.join(root, 'outSeason'))
            
            outfileNameSeason = 'season_' + total_Daily_Files[i]
            outFolderSeason = os.path.join(root, 'outSeason')
            outputFileSeason = os.path.join(outFolderSeason, outfileNameSeason)
            
            outFilesFinal = []
            for filename in os.walk(outFolderSeason):
                outFilesFinal = filename[2]
                iii = len(outFilesFinal)
                if os.path.isfile(outputFileSeason):
                    newOutFileNameSeason = outputFileSeason[0 : -4] + '_' + str(iii) + '.csv'
                    dfFinalSeason.to_csv(newOutFileNameSeason, index = False)
                else: 
                    dfFinalSeason.to_csv(outputFileSeason, index = False)

            print('End of all calculations')


        #return {'S_Ave_GoodDay' : AveragesumRows}
        return {'S_Ave_GoodDay' : AveragesumRows, 'GCM_RCM' : climateModel, 'y2' : dfpcpCol[climateModel], 'S_GoodDay' : sumRows}






# Step 4: EMA_Workbench connector
'''
Created on 20 dec. 2010

This file illustrated the use the EMA classes for a contrived example
It's main purpose has been to test the parallel processing functionality

.. codeauthor:: jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>
'''


from ema_workbench import (Model, RealParameter, Constant, ScalarOutcome, ema_logging, IntegerParameter,
                          CategoricalParameter, perform_experiments, TimeSeriesOutcome, ArrayOutcome)

from ema_workbench import (MultiprocessingEvaluator)

### import time
start_time = time.time()

if __name__ == '__main__':
    ema_logging.LOG_FORMAT = '[%(name)s/%(levelname)s/%(processName)s] %(message)s'
    ema_logging.log_to_stderr(ema_logging.INFO)

    model = Model('UZHModel', function = HDNs_Model)  # instantiate the model
    
    
    # specify process model parameters  xRCP=None, xClimateModel=None
    model.uncertainties = [RealParameter("Xfactor1",  0.51, 3.49),
                            IntegerParameter ("xRCP", 1,3),  
                            #RealParameter("xRCP", 0.51, 3.49),
                           RealParameter("xClimateModel", 0, 1),
                           ]
    
    # specify polices IntegerParameter
    model.levers = [
                    RealParameter("x1TmaxThershold", -8.0, -6.0),
                    RealParameter("x2TminThershold", -10.0, -8.0)]
   

    # specify outcomes
    model.outcomes = [ScalarOutcome('S_Ave_GoodDay'),
                      ScalarOutcome('GCM_RCM'),
                      ArrayOutcome('S_GoodDay')

                      ]

    results = perform_experiments(model, 3, 2)

