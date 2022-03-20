import sys

def main():
    if len(sys.argv)<2:
        print("debe introducir el nombre del archivo")
        sys.exit()
    else:
        abstractData(sys.argv)
        
def abstractData(input):
    filename= input[1]
    file1=open(filename,"r")
    file2=file1.readlines()
    file1.close()
    convertData (file2)
   
def convertData(list):
    problemMatrix=[]
    method=0
    optimization=""
    descitionVar = 0
    restrictionNum= 0
    objetiveFuction=[]
    count= 0

    while list!=[]:
        if count >=2:
            row=list[0].rstrip()
            row1=row.rstrip(",")
            sub=row1.split(",")
            problemMatrix=problemMatrix+[sub]
            count+=1
            list=list[1:]
        
        elif count ==0:
            row=list[0].rstrip()
            row1=row.rstrip(",")
            sub=row1.split(",")
            method=int(sub[0])
            optimization= sub[1]
            descitionVar = int(sub[2])
            restrictionNum= int(sub[3])
            count+=1
            list=list[1:]
        else:
            row=list[0].rstrip()
            row1=row.rstrip(",")
            sub=row1.split(",")
            objetiveFuction=sub
            count+=1
            list=list[1:]
    print ("objetiveFuction",objetiveFuction)
    print ("problemMatrix",problemMatrix)
    print (" method", method)
    print (" optimization", optimization)
    print (" restrictionNum", restrictionNum)
    print (" descitionVar", descitionVar)

main()

