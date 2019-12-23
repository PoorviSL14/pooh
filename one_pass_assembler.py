scode=open("CODE.txt",'r').readlines()                         #SOURCE PROGRAM
otab=open("OPTAB.txt",'r').readlines() 			       #OPERAND TABLE                                   
ocode=open("OBJECT.txt",'w')    		               #OBJECT PROGRAM                                         
stab=open("SYMTAB.txt",'w')                                     #SYMBOL TABLE                                             
optab={}
symtab={}
fref={}
obc=[]
locctr=0     
#CODE TO STORE MNEMONIC OPERANDS                        
for line in otab:
    op=line.split()
    optab.update({op[0]:op[1]})

first=scode[0]                              #READ FIRST LINE OF SOURCE PROGRAM
if "START" in first:
    name,mo,opr=first.split(" ")
    saddr=opr[:len(opr)-1]                         #SAVE THE STARTING ADDTRESS
    locctr=hex(int(saddr,16)) #INITIALIZE LOCATION COUNTER TO STARTING ADDRESS 
else:
    locctr=0                              #INITIALIZE LOCATION COUNTER TO ZERO
for i in range(1,len(scode)):
    line=scode[i]
    la,mo,opr=line.split(" ")
    opr=opr[:len(opr)-1]
    if mo=="END":                                       #END OF SOURCE PROGRAM
        break

    #NO SYMBOL IN LABEL FIELD
    if la=="-":                        
        if mo in optab:                            #SEARCH FOR OPCODE IN OPTAB
            x=optab[mo]
            if opr in symtab:                    #SEARCH FOR OPERAND IN SYMTAB
                if symtab[opr]!="*":                 #SYMBOL VALUE IS NOT NULL
                    y=symtab[opr]        #OPERAND ADDRESS WILL BE SYMBOL VALUE
                    obc.append("#"+locctr[2:]+"#"+x+y)
                else:                  #SYMBOL VALUE IS NULL(UNDEFINED SYMBOL)
                    obc.append("#"+locctr[2:]+"#"+x+'0000')    
                                                  #USE ZERO AS OPERAND ADDRESS
                    madd=str(hex(int(locctr,16)+1))                        
                    fref[opr]=[]
                    fref[opr].append(madd[2:])
                                           #STORE ADDRESS OF FORWARD REFERENCE
            else:                                       #OPERAND NOT IN SYMTAB
                symtab[opr]="*"       #INSERT SYMBOL TO SYMTAB WITH NULL VALUE
                madd=str(hex(int(locctr,16)+1))
                fref[opr]=[]
                fref[opr].append(madd[2:]) #STORE ADDRESS OF FORWARD REFERENCE
                obc.append("#"+locctr[2:]+"#"+x+'0000')   
                                                  #USE ZERO AS OPERAND ADDRESS 
#INCREMENT THE LOCATION COUNTER TO POINT TO NEXT INSTRUCION OF THE SOURCE CODE
        locctr=str(hex(int(locctr,16)+3))
    #SYMBOL IN LABEL FIELD
    else:
        temp=str(locctr) 
        temp=temp[2:]                               #STORE LOCATION COUNTER AS     
        symtab[la]=temp.replace("\n","")               #SYMBOL VALUE IN SYMTAB
        if la in fref:                       #IF FORWARD REFERENCE ARE PRESENT
            for item in fref[la]:                                               
                obc.append("$"+str(item)+"$"+temp)  
                                           #OBJECT CODE FOR FORWARD REFERENCES
        if mo in optab:                            #SEARCH FOR OPCODE IN OPTAB
            x=optab[mo]
            if opr in symtab:                    #SEARCH FOR OPERAND IN SYMTAB
                if symtab[opr]!="*":                 #SYMBOL VALUE IS NOT NULL
                    y=symtab[opr]        #OPERAND ADDRESS WILL BE SYMBOL VALUE
                    obc.append("#"+temp[2:]+"#"+x+y)                                
                else:                  #SYMBOL VALUE IS NULL(UNDEFINED SYMBOL)
                    obc.append("#"+temp[2:]+"#"+x+'0000')                         
                                                  #USE ZERO AS OPERAND ADDRESS
                    madd=str(hex(int(locctr,16)+1))
                    fref[opr]=[]
                    fref[opr].append(madd[2:])
                                           #STORE ADDRESS OF FORWARD REFERENCE
            else:                                       #OPERAND NOT IN SYMTAB
                symtab[opr]="*"       #INSERT SYMBOL TO SYMTAB WITH NULL VALUE
                madd=str(hex(int(locctr,16)+1))
                fref[opr]=[]
                fref[opr].append(madd[2:]) #STORE ADDRESS OF FORWARD REFERENCE
                obc.append("#"+temp[2:]+"#"+x+'0000')                             
                                                  #USE ZERO AS OPERAND ADDRESS
#INCREMENT THE LOCATION COUNTER TO POINT TO NEXT INSTRUCION OF THE SOURCE CODE
            locctr=str(hex(int(locctr,16)+3))
        #DEFINITION OF VARIABLES
        elif mo=="RESW":                        #RESERVE INDICATED NO OF WORDS
            locctr=str(hex(int(locctr,16) + int(opr)*3))
            obc.append("-")
        elif mo=="RESB":                        #RESERVE INDICATED NO OF BYTES
            locctr=str(hex(int(locctr,16) +int(opr)))
            obc.append("-")
        #DEFINITION OF CONSTANTS
        elif mo=="WORD":
            obc.append('00'+hex(int(opr)))          #ONE WORD INTEGER CONSTANT
            locctr=str(hex(int(locctr,16)+3))
        elif mo=="BYTE":
            if opr[0]=="X":                              #HEXADECIMAL CONSTANT
                temp1=(len(opr)-3)/2
                locctr=str(hex(int(locctr,16)+temp1))
                temp2=opr[2:len(opr)-1]
                obc.append(temp2)
            elif opr[0]=="C":                              #CHARACTER CONSTANT
                temp1=(len(opr)-3)*2
                locctr=str(hex(int(locctr,16)+temp1))
                temp2=opr[2:len(opr)-1]
                s=""
                for i in temp2:
                    s=s+str(hex(ord(i)))
                obc.append(s)
plen=str(hex(int(locctr,16)-int(saddr,16)))                    #PROGRAM LENGTH 
print("SOURCE PROGRAM:",scode,"\n")
print("OPERAND TABLE:",optab,"\n")
print("OBJECT CODE:",obc,"\n")
print("SYMBOL TABLE:",symtab,"\n")
print("FORWARD REFRENCES:",fref,"\n")
print("Program length:",plen,"\n")


#WRITING SYMTAB TO FILE
for (i,j) in symtab.items():
    stab.write(str(i) + " " + str(j) +"\n")
stab.close()

#WRITING OBCECT CODE TO OBJECT PROGRAM
ocode.write("H^"+str(name)+"  ^00"+str(saddr)+"^"+str(plen))    #HEADER RECORD
n=0
i=0
while(i<len(obc)):                                                #TEXT RECORD
    rec=str(obc[i])
    if obc[i]=="-":                          #NO TEXT RECORD FOR RESW AND RESB
        n=0                                                   #NEW TWXT RECORD
        i=i+1
        continue
    elif rec[0]=="$":                      #TEXT RECORD FOR FORWARD REFERENCES
        n=0                                                   #NEW TEXT RECORD
        rec=str(obc[i])
        ocode.write("\nT^"+rec[1:5]+"^02^"+rec[6:])
        i=i+1
    else:                            #WRITE THE OBJECT CODE IN THE TEXT RECORD
        if n==0:                        #IF IT FITS IN THE CURRENT TEXT RECORD
            ocode.write("\nT^"+rec[1:5])      #ELSE INITIALIZE NEW TEXT RECORD
            p=0
            k=i
            while(obc[k]!="-" and obc[k][0]!="$" and k<len(obc)-1):            
                k=k+1                                                          
                p=p+1
            l=hex(p*3)
            l=l[2:]
            ocode.write("^0"+l)
            for j in range(i,k):
                ocode.write("^"+str(obc[j][6:]))
                n=n+1
            i=k
        else:
            ocode.write("^"+rec)
            i=i+1
            n=n+1
ocode.write("\nE^"+str(saddr))                                     #END RECORD
ocode.close()
 



 
