import sys
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
    problemMatrix=[]
    method=0
    optimization=""
    descitionVar = 0
    restrictionNum= 0
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
                restrictionNum= int(sub[3])
                count+=1
            else:
                row1=row.rstrip()
                sub=row1.split(",")
                objetiveFuction=sub
                count+=1
 #examples of format:
 # objetiveFuction: ['3', '5'] 
 # resticction Matrix [['2', '1', '<=', '6'], ['-1', '3', '<=', '9'], ['0', '1', '<=', '4']]    
 # method number: 0 
 # optimization type: max  
 # number of restrictions: 3
 # number of decision variables: 2  
    print ("objetiveFuction",objetiveFuction)
    print ("problemMatrix",problemMatrix)
    print (" method", method)
    print (" optimization", optimization)
    print (" restrictionNum", restrictionNum)
    print (" descitionVar", descitionVar)
main()


