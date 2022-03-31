from array import array
import sys
from turtle import clear
#Global variables
method=0
optimization=""
descitionVar = 0
restrictionNum= 0
totalVars=0
BasicVariables=[]
ArtifitialVar=[]
bounded=True
degenerate=False
#funtion 1:main
#verifies that any parameters other than the name of the
# program have been entered
def main():
    info=["\nThis program seeks to solve the problems of maximization and minimization of linear programming,",
    "using the Simplex, Big M and Two Phase methods \n ",
    "The file will be executed by calling simplex.py in the following two ways  ",
    "\t python simplex.py [-h] archivo.txt ",
    "\t python simplex.py archivo.txt \n", 
    "The structure of the input file (plain text with elements separated by commas) must contain: ",
    "method, optimization type, Number of decision variables, Number of constraints ",
    "objective function coefficients ",
    "constraint coefficients and constraint sign \n",
    "The method will be represented as follows (by numbers): ",
    "0=Simplex, 1=Big M, 2=Two Phase \n "]
    if len(sys.argv)<2 or len(sys.argv)>3:
        
        print("must have introduce the name of the file too")
        sys.exit()
    else:
        if len(sys.argv)==3:
            for i in info:
                print (i)
            abstractImputData(sys.argv,2)

        else:
            abstractImputData(sys.argv,1)

#funtion 2: abstractImputData
#obtein the name of the txt file
def abstractImputData(input,position):
    global filename
    filename= input[position]
    abstractData(filename)

#funtion 3: abstractImputData
# convert the txt information into
# a list with coefficients for the objective function
# a matrix with the restricctions
#and the values of the method, optimization type, number of decision variables, number of restrictions
def abstractData(file):
    global  method,optimization,descitionVar,restrictionNum,totalVars
    problemMatrix=[]
    objetiveFuction=[]
    count= 0
    with open (file) as fileObject:
        for row  in fileObject:
            if count >=2:
                row1=row.rstrip()
                sub=row1.split(",")
                problemMatrix=problemMatrix+[sub]
                count+=1
            elif count ==0:
                sub=row.split(",")
                method=int(sub[0])
                optimization= sub[1]
                descitionVar = int(sub[2])
                restrictionNum = int(sub[3])
                count+=1
            else:
                row1=row.rstrip()
                sub=row1.split(",")
                objetiveFuction=sub
                count+=1 
    problemMatrix=convertValMatrix(problemMatrix)
    objetiveFuction=ConvertValList(objetiveFuction)
    menu(problemMatrix,objetiveFuction)

#funtion 4: menu
#determines to which method to send the matrix to solve
def menu(problemMatrix,objetiveFuction):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,PhaseTwo
    if optimization =="min":
        objetiveFuction= changeSymbols(objetiveFuction)
    
    problemMatrix=verifyRightSide(problemMatrix)
    if method ==1 or method == 0:
        if checkMethod(problemMatrix)==False:
            if method==1:
                method=0
            else:
                method=1
    aumentedVar= detNumberOfVariables(problemMatrix)
    totalVars= descitionVar + aumentedVar
    if method ==0:
        aumentedMat=[]
        aumentedMat=aumentedMatrixSimplex(problemMatrix,objetiveFuction)
        BasicVariables=initialBV(totalVars)
        PhaseTwo=False
        simplex(aumentedMat)
    elif method==1:
        print("NO ES SIMPLEX")
    else:
        TwoPhases(problemMatrix,objetiveFuction)
       
# funtion 5: simplex
#calls and starts the functions needed to do the
#  simplex method  
def simplex(aumentedMat):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,PhaseTwo
    row_column=[]
    flag=True
    currentMat=aumentedMat
    row_column=getPivot(currentMat)
    

    printCosole(currentMat,0,"w","Initial Matrix")
    iterationNum=1
    while flag:
        if bounded==False:
            flag=False
            print(currentMat,"Not bounded Matrix","\n")
            printCosole(currentMat,iterationNum-1,"a","Not bounded Matrix")
        else:
            if its0ptimum(currentMat):
                flag=False
                if method==2:
                    printCosole(currentMat,iterationNum-1,"a","Optimun Matrix")
                    return currentMat
                else:
                    printCosole(currentMat,iterationNum-1,"a","Optimun Matrix")
                    #verificar si tiene multiple solucion
                
            else:
                row_column=getPivot(currentMat)
                currentMat=iteration(currentMat,row_column)
                printCosole(currentMat,iterationNum,"a","Current Matrix")
                iterationNum+=1

#funtion 6: checkMethod
#validates that the indicated method 
# to solve the problem is the correct one
def checkMethod(problemMatrix):
    global  method,optimization,descitionVar,restrictionNum,totalVars
    count=0
    if method==0:
        for i in problemMatrix:
            count = 0
            for j in i:
                if count == descitionVar:   
                    if j== ">=" or j=="=":
                        return False 
                count+=1
        return True
    else:
        if  method==1:
            for i in problemMatrix:
                count = 0
                for j in i:
                    if count == descitionVar:   
                        if j== ">=" or j=="=":
                            return True 
                    count+=1
            return False

#funtion 7: ConvertValList
#convert values stored in a list
#  from string to float
def ConvertValList(list):
    newList=[]
    for i in list:
        newList.append(float(i))
    return newList

#funtion 8: convertValMatrix
#convert coefficients of array,
#  from string to floats
def convertValMatrix(matrix):
    global  descitionVar
    count = 0
    OmitColum= descitionVar
    newMat= []
    for i in  matrix:
        count = 0
        row=[]
        for j in i:
            if count != OmitColum:
                row.append(float(j))
            else:
                row.append(j)
            count+=1
        newMat.append(row)
    return newMat
#funtion 9: detNumberOfVariables
#determines how many extra variables
#  the augmented matrix will have
def detNumberOfVariables(restrictionMat):
    global  descitionVar
    newvars=0
    count=0
    for i in restrictionMat:
        count = 0
        for j in i:
            if count == descitionVar:   
                if j== ">=":
                    newvars+=2
                else:
                    newvars+=1
            count+=1
    return newvars
#function 10:aumentedMatrixSimplex
#return the aumented matrix in the simplex method            
def aumentedMatrixSimplex(restriction,objective):
    global  descitionVar,totalVars
    aumentedMat=[] 
    array=[]
    count2=0
    while count2<=totalVars:
        if count2 <(len(objective)):
            array.append(-(objective[count2]))
        else:
            array.append(float(0))
        count2+=1
    aumentedMat.append(array)
    
    count=0
    for i in restriction:
        j=0
        array1=[]
        while j <totalVars:
            if j <descitionVar:
                array1.append(i[j])
                j+=1
            elif j== descitionVar+count:
                array1.append(float(1)) 
                j+=1
            else:
                array1.append(float(0))
                j+=1
        array1.append(i[-1])
        aumentedMat.append(array1)
        count+=1
    return(aumentedMat)

#function 11: initialBV
#obtein de basic variables of the 
# iteration 0 in a simplex method   
def initialBV(totalVar):
    global descitionVar
    i=descitionVar+1
    BasicVars=[]
    while i<= totalVar:
        BasicVars.append (i) 
        i+=1 
    return(BasicVars)
#function 12: its0ptimum 
#determinate if the matrix is optimun                
def its0ptimum(matrix):
    row0= matrix[0]
    row= row0[0:len(row0)-2]
    for i in row:
        if i < 0:
            return False
    return True
#function 13: getPivot 
#obtein the position of the pivot
def getPivot(matrix):
    global bounded,degenerate
    row=1
    column=0
    count=0
    count1=1
    currentRow=0
    for i  in matrix:
        if currentRow==0:
            objective=matrix[0]
            for i in objective[0:-2]:
                if i< matrix[0][column]:
                    column=count
                count+=1
            count=0
        else:
            if i[column]== float(0):
                count1+=1
                if row ==1:
                    row=count1
            else:
                if ((i[-1]/i[column]) < ((matrix[row][-1])/(matrix[row][column])) and (i[-1]/i[column])>=float(0)):
                    row=count1
                count1+=1
        currentRow+=1
    if row==1:
        if matrix[row][column]==float(0) or (matrix[row][-1]/matrix[row][column])<float(0):
            bounded=False
        else:
            return ([row,column])
    
    return ([row,column])
#function 14: iteration
#make the iterations in the simplex method
def iteration(matrix,pivot):
    global BasicVariables
    newRow=[]
    IterationMatrix= []
    numPivot=matrix[pivot[0]][pivot[1]]
    count=0
    for i in matrix[pivot[0]]:
        newRow.append(round(float(i/numPivot),3))
    for i in matrix:
        array=[]
        if count== pivot[0]:
            IterationMatrix.append(newRow)
        else:
            currentCol=0
            for j in i:
                val=j-(matrix[count][pivot[1]])*(newRow[currentCol])
                array.append(round(float(val),3))
                currentCol+=1
            IterationMatrix.append(array)
        count+=1
    BasicVariables[pivot[0]-1]=pivot[1]+1
    return (IterationMatrix)
#function 15: printCosole
#prints in console and in a txt the solution 
# of the linear problem with the simplex method
def printCosole(matrix,iterationNum,action,message):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,filename,PhaseTwo
    if PhaseTwo==True:
        action="a"
    else:
        action=action
    columnNames=[]
    columnNames.append("VB")
    i=0
    while i < totalVars:
        columnNames.append("X"+str(i+1))
        i+=1
    columnNames.append("LD")
    printMatrix=[]
    count=0
    for i in matrix:
        array=[]
        if count==0:
            if optimization=="min":
                array.append("-U")
            else:
                array.append("U")
        else:   
            array.append("X"+str(BasicVariables[count-1]))
        for j in i: 
            array.append(j)
        count+=1
        printMatrix.append(array)
    
    stringChain=""
    stringChain+= message + "\n"
    stringChain+= "Iteration :" + str(iterationNum)+ "\n"
    for j in columnNames:
            stringChain+=str(j)+"\t\t     "
    stringChain+="\n"
    for i in printMatrix:
        for j in i:
            stringChain+=str(j)+"\t\t   "
        stringChain+="\n"
    stringChain+="\n\n"
    print(stringChain)
    name=str(filename[0:-4])+"_solution.txt" 
    file= open(name,action)
    file.write(stringChain)
    file.close()
#function 16: changeSymbols
#change the symbols of the coefficients in a list
def changeSymbols(list):
    newList=[] 
    for i in list:
        newList.append(-i) 
    return newList
#function 17: verifyRightSide
#change the symbols of the coefficients 
# and the form of equality 
# if the right side is negative
def verifyRightSide(matrix):
    global  descitionVar
    newMatrix=[]
    for i in matrix:
        array=[]
        count=0
        if i[-1]<0:
            for j in i:
                if count== descitionVar:
                    if j=="<=":
                        array.append(">=")
                    elif j==">=":
                        array.append("<=")
                    else:
                        array.append("=")
                else:
                    array.append(-j)
                count+=1
            newMatrix.append(array)
        else:
            newMatrix.append(i)
   
    return (newMatrix)
###################################################################
# funtion 18: TwoPhases
#calls and starts the functions needed to do the
#  TwoPhase method 
def TwoPhases(problemMatrix,objetiveFuction):
    global BasicVariables,PhaseTwo,filename
    PhaseTwo=False
    aumentedMat=[]
    aumentedMat=aumentedMatrixTwoPhases(problemMatrix)
    properAumentedMat=properWay(aumentedMat)
    #primera fase
    print("First Phase")
    aumentedObjectiveFuntion=[]
    i=0
    while i<=totalVars:
        if i <(len(objetiveFuction)):
            aumentedObjectiveFuntion.append(-(objetiveFuction[i]))
        else:
            aumentedObjectiveFuntion.append(float(0))
        i+=1
    
    FirstPhaseMat=simplex(properAumentedMat)
    aumentedMatrix=prepareSeconPhase(FirstPhaseMat,aumentedObjectiveFuntion)
    stringChain=""
    stringChain+=  "Preparing second phase\n"
    stringChain+= "substitute objective function\n"
    stringChain+="\n\n"
    stringChain+= "Second Phase\n"
    name=str(filename[0:-4])+"_solution.txt" 
    file= open(name,"a")
    file.write(stringChain)
    file.close()
    print("Second Phase")
    PhaseTwo=True
    aumentedMatrix=simplex(aumentedMatrix)
# funtion 20: prepareSeconPhase
#preparation for phase two where the objective function is introduced, 
# the artificial variables are removed and the values ​​
# "that the method does not like" are subtracted
def prepareSeconPhase(FirstPhaseMat,objetiveFuction):
    global method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,filename,ArtifitialVar
    newAumentedMat=[]
    count=0
    for i in FirstPhaseMat:
        if count==0:
            newAumentedMat.append(objetiveFuction)
        else:
            newAumentedMat.append(i)
        count+=1
    newAumentedMat=fixBasicVarObjective(newAumentedMat)
    aumentedMatrix=withdrawArtifitial(newAumentedMat)
    return(aumentedMatrix)

# funtion 21: fixBasicVarObjective
#remove the values ​​of the basic variables that 
# the method doesn't like on line 0
def fixBasicVarObjective(newAumentedMat):
    global method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,filename,ArtifitialVar
    count=0
    answerMatrix=[]
    objectivelist=newAumentedMat[0]
    i=0
    while i < len(BasicVariables):
        col=BasicVariables[i]-1
        row=0
        count=0
        for j in newAumentedMat:
            if count==0:
                count+=1
            else:
                if j[col] ==float(1):
                    row=count   
                count+=1
        array=[]
        currentCol=0
        for value in objectivelist:
            val=value-(objectivelist[col])*(newAumentedMat[row][currentCol])
            array.append(round(float(val),3))
            currentCol+=1
        objectivelist=array
        i+=1
    current=0
    for list in newAumentedMat:
            if current==0:
                answerMatrix.append(objectivelist)
            else:
                answerMatrix.append(list)  
            current+=1
    return(answerMatrix)

# funtion 22: withdrawArtifitial
#delete the columns(coefficients)
# of the artifitial variables
def withdrawArtifitial(newAumentedMat):
    global method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,filename,ArtifitialVar
    resMatrix=[]
    matrix=newAumentedMat
    count=0
    while count < len(ArtifitialVar):
        for i in matrix:
            array=[]
            currentJ=0
            for j in i:
                if currentJ==ArtifitialVar[count]-1:
                    array.append(float(0)) 
                else:
                    array.append(j)
                currentJ+=1
            resMatrix.append(array)
        matrix=resMatrix
        resMatrix=[]
        count+=1
    
    return(matrix)       

# funtion 23: properWay
#changes the values ​​of the objective function 
# to the appropriate form (without the artificial variables)
def properWay(aumentedMat):
    global  descitionVar,totalVars,ArtifitialVar
    ProperMat=[]
    ProperObjective=[]
    count=0
    current=0
    for i in aumentedMat:
        if count==0:
            ProperMat.append(i)
        else:
            if i[ArtifitialVar[current]-1] ==float(1):
                ProperMat.append(i)
                current+=1
        count+=1
    j=0
    while j < len(ProperMat[0]):
        i=1
        res=ProperMat[0][j]
        while i< len(ProperMat):
            res= res-(ProperMat[i][j])
            i+=1
        ProperObjective.append(float(res))
        j+=1

    ProperMat=[]
    count=0
    current=0
    for i in aumentedMat:
        if count==0:
            ProperMat.append(ProperObjective)
        else:
            ProperMat.append(i)      
        count+=1
    return(ProperMat)
#function24:aumentedMatrixTwoPhases
#return the aumented matrix in the two Phase method 
def aumentedMatrixTwoPhases(restriction):
    global  descitionVar,totalVars,ArtifitialVar
    aumentedMat=[] 
    count=0
    AuMat=[]
    for i in restriction:
        j=0
        array1=[]
        while j <totalVars:
            if j <descitionVar:
                array1.append(i[j])
                j+=1
            elif j== descitionVar+count:
                if i[descitionVar]=="<=":
                    array1.append(float(1)) 
                    j+=1
                    BasicVariables.append((descitionVar)+count+1)  
                elif i[descitionVar]=="=":
                    array1.append(float(1)) 
                    j+=1
                    BasicVariables.append((descitionVar)+count+1)
                    ArtifitialVar.append((descitionVar)+count+1)
                else:
                    array1.append(float(-1))
                    array1.append(float(1))
                    j+=2
                    count+=1
                    ArtifitialVar.append((descitionVar-1)+count+2)
                    BasicVariables.append((descitionVar-1)+count+2)
            else:
                array1.append(float(0))
                j+=1
        array1.append(i[-1])
        aumentedMat.append(array1)
        count+=1
    count2=0
    i=0
    array=[]  
    while i < totalVars:  
        if count2<(len(ArtifitialVar)):
            current=ArtifitialVar[count2]
            if i== (current-1):
                array.append(float(1))
                count2+=1
            else:
                array.append(float(0))
            i+=1
        else:
            array.append(float(0))
            i+=1
    array.append(float(0))
    AuMat.append(array)
    for i in aumentedMat:
        AuMat.append(i)
    return(AuMat)

main()
