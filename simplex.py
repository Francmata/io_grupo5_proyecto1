import sys
#Global variables
method=0
optimization=""
descitionVar = 0
restrictionNum= 0
totalVars=0
BasicVariables=[]
#funtion 1:main
#verifies that any parameters other than the name of the
# program have been entered
def main():
    if len(sys.argv)<2:
        print("must have introduce the name of the file too")
        sys.exit()
    else:
        abstractImputData(sys.argv)

#funtion 2: abstractImputData
#obtein the name of the txt file
def abstractImputData(input):
    filename= input[1]
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
    global  method,optimization,descitionVar,restrictionNum,totalVars
    if method ==1 or method == 0:
        if checkMethod==False:
            if method==1:
                method=0
            else:
                method=1
    aumentedVar= detNumberOfVariables(problemMatrix)
    totalVars= descitionVar + aumentedVar
    if method ==0:
        simplex(problemMatrix,objetiveFuction)

# funtion 5: simplex
#calls and starts the functions needed to do the
#  simplex method  
def simplex(problemMatrix,objetiveFuction):
    global  method,optimization,descitionVar,restrictionNum,totalVars,BasicVariables
    aumentedMat=[]
    aumentedMat=aumentedMatrixSimplex(problemMatrix,objetiveFuction)
    row_column=[]
    
    flag=True
    BasicVariables=initialBV(totalVars)
    currentMat=aumentedMat
    while flag:
        
        if its0ptimum(currentMat):
            flag=False
            print(currentMat,"OptimunMatrix","\n")
            #Hacer funcion de print en txt 
        else:
            row_column=getPivot(currentMat)
            currentMat=iteration(currentMat,row_column)
            print(currentMat,"currentMat","\n")

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
#  from string to integer
def ConvertValList(list):
    newList=[]
    for i in list:
        newList.append(int(i))
    return newList

#funtion 8: convertValMatrix
#convert coefficients of array,
#  from string to integers
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
                row.append(int(j))
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

            if i[column]==0:
                count1+=1
            else:
                if ((i[-1]/i[column]) < ((matrix[row][-1])/(matrix[row][column])) and (i[-1]/i[column])>=0):
                    row=count1
                count1+=1
        currentRow+=1
    return ([row,column])
#function 14: iteration
#make yhe iterations in the simplex method
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
   
main()


