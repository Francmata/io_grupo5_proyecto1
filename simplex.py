import sys
from turtle import clear
#Global variables
method=0
optimization=""
descitionVar = 0
restrictionNum= 0
totalVars=0
BasicVariables=[]
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
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables
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
        simplex(aumentedMat)
    else:
        print("NO ES SIMPLEX")

# funtion 5: simplex
#calls and starts the functions needed to do the
#  simplex method  
def simplex(aumentedMat):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded
    row_column=[]
    flag=True
    currentMat=aumentedMat
    #row_column=getPivot(currentMat)
    printCosole(currentMat,0,"w","Initial Matrix")
    iterationNum=1
    while flag:
        if bounded==False:
            flag=False
            print(currentMat,"Not bounded Matrix","\n")
            printCosole(currentMat,iterationNum-1,"a","Not bounded Matrix")
            
        #elif degenerate == True:
        #    print(currentMat,"Not bounded Matrix","\n")
        #    print("solucion degenerada")
        #    row_column=getPivot(currentMat)
        #    currentMat=iteration(currentMat,row_column)
        #    print(currentMat,"currentMat","\n")
        else:
            if its0ptimum(currentMat):
                flag=False
                
                printCosole(currentMat,iterationNum-1,"a","Optimun Matrix")
                #verificar si tiene multiple solucion
                
            else:
                row_column=getPivot(currentMat)
                currentMat=iteration(currentMat,row_column)
               
                printCosole(currentMat,iterationNum,"a","Current Matrix")
                #row_column=getPivot(currentMat)
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
            array.append(0)
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
                array1.append(1) 
                j+=1
            else:
                array1.append(0)
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
            for i in matrix[0]:
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
                #if ((i[-1]/i[column]) == ((matrix[row][-1])/(matrix[row][column]))):
                #    degenerate=True

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
        newRow.append(round(float(i/numPivot),5))
    for i in matrix:
        array=[]
        if count== pivot[0]:
            IterationMatrix.append(newRow)
        else:
            currentCol=0
            for j in i:
                val=j-(matrix[count][pivot[1]])*(newRow[currentCol])
                array.append(round(float(val),5))
                currentCol+=1
            IterationMatrix.append(array)
        count+=1
    BasicVariables[pivot[0]-1]=pivot[1]+1
    return (IterationMatrix)
#function 15: printCosole
#prints in console and in a txt the solution 
# of the linear problem with the simplex method
def printCosole(matrix,iterationNum,action,message):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables,bounded,filename
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
    #stringChain+="\n Input variable: "+"X"+str(pivot[1]+1)
    #stringChain+="\n Outgoing variable: "+"X"+str(BasicVariables[pivot[0]-1])
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
    print(newMatrix)
    return (newMatrix)


main()


