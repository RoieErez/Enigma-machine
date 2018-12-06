Alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Rotor1=['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
Rotor2=['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E']
Rotor3=['B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q','O']
Rotor4=['E','S','O','V','P','Z','J','A','Y','Q','U','I','R','H','X','L','N','F','T','G','K','D','C','M','W','B']
Rotor5=['V','Z','B','R','G','I','T','Y','U','P','S','D','N','H','L','X','A','W','M','J','Q','O','F','E','C','K']
Turnover={1:17,2:5,3:22,4:10,5:26}

class Reflector:
    def __init__(self):
        self.Ref=['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T']
    def output(self,input):
        return self.Ref[Alphabet.index(input)]
 
class Rotor:
    def __init__(self,RotorType,Offset,Setting): 
        self.Type=RotorType
        if self.Type==1:
            self.Rtr=Rotor1
        if self.Type==2:
            self.Rtr=Rotor2
        if self.Type==3:
            self.Rtr=Rotor3
        if self.Type==4:
            self.Rtr=Rotor4
        if self.Type==5:
            self.Rtr=Rotor5   
        self.Notch = False 
        if Offset==  Turnover[RotorType] :    self.Notch=True
          
        self.B=Offset
        self.C=Setting                        
    def Forward(self,input):
        self.A=Alphabet.index(input)+1   
        x=self.A+self.B-self.C   
        if x >26 or x<0:
            x=x%26 
        return Alphabet[(Alphabet.index(self.Rtr[x-1])+1-self.B+self.C)%26-1]
    def Reverse(self,input):
        self.A=Alphabet.index(input)+1
        x=self.A+self.B-self.C
        if x >26 or x<0:
            x=x%26   
        return Alphabet[(self.Rtr.index(Alphabet[x-1])+1-self.B+self.C)%26-1]

class Plugboard:
    def __init__(self,Pb):
        self.Pb=Pb
    def Plugset(self,char): 
        if char in self.Pb:
            return self.Pb[char]
        return char

class Machine:
    def __init__(self,type1,type2,type3,offset1,offset2,offset3,setting1,setting2,setting3,pb): 
        self.Rotors=[Rotor(type1,offset1,setting1),Rotor(type2,offset2,setting2),Rotor(type3,offset3,setting3)]
        self.reflector=Reflector()    # type1=left type2=middle type3=right
        self.plugboard=pb   #     [0]         [1]         [2]

    def checkNotch(self):             # B is set for the offset and C is the setting
        self.Rotors[0].Notch=False
        self.Rotors[1].Notch=False
        self.Rotors[2].Notch=False
        if Turnover[self.Rotors[0].Type] == self.Rotors[0].B: 
            self.Rotors[0].Notch=True
        if Turnover[self.Rotors[1].Type] == self.Rotors[1].B:
            self.Rotors[1].Notch=True
        if Turnover[self.Rotors[2].Type] == self.Rotors[2].B:
            self.Rotors[2].Notch=True

    def moveOffset(self):
        if self.Rotors[2].Notch or self.Rotors[1].Notch :
            if self.Rotors[1].Notch:
                self.Rotors[0].B+=1 
            self.Rotors[1].B+=1
        self.Rotors[2].B+=1
        if self.Rotors[0].B>26 or self.Rotors[0].B<0:
            self.Rotors[0].B=self.Rotors[0].B%26
        if self.Rotors[1].B>26 or self.Rotors[1].B<0:
            self.Rotors[1].B=self.Rotors[1].B%26
        if self.Rotors[2].B>26 or self.Rotors[2].B<0:
            self.Rotors[2].B=self.Rotors[2].B%26
        if self.Rotors[0].B==0:
            self.Rotors[0].B=26
        if self.Rotors[1].B==0:
            self.Rotors[1].B=26
        if self.Rotors[2].B==0:
            self.Rotors[2].B=26         
    
    def Encr(self):
        userInput=input('Enter a string to encrypt: (big letters): ')
        encText=list(userInput)
        def hasNumbers(inputString):
            return any(char.isdigit() for char in inputString) 
        if hasNumbers (userInput):
            print('NOTE! you can only use letters in the Enigma machine please try again!!!')
            return
        encText= [x for x in encText if x != ' ']
        res2=""
        for x in encText:  # x the user input
            x.capitalize()
            self.moveOffset()
            self.checkNotch()  
            res=self.plugboard.Plugset(x.capitalize())   #plugbord               
            res=self.Rotors[2].Forward(res)       
            res=self.Rotors[1].Forward(res)
            res=self.Rotors[0].Forward(res)            
            res=self.reflector.output(res)            
            res=self.Rotors[0].Reverse(res)            
            res=self.Rotors[1].Reverse(res)
            res=self.Rotors[2].Reverse(res)
            res=self.plugboard.Plugset(res) #plugbord
            res2+=res            
        print(res2)

print("Wellcome To the Enigma Machine !...")
left=input("Enter the LEFT roter number : (1-5)")
middle=input("Enter the MIDDLE roter number : (1-5)")
right=input("Enter the RIGHT roter number : (1-5)")
setLeft=input("Enter Roter LEFT Setting (numbers only) :  ")
setMiddle=input("Enter Roter MIDDLE Setting (numbers only):  ")
setRight=input("Enter Roter RIGHT Setting (numbers only):  ")
OfsetLeft=input("Enter Roter LEFT Offset (numbers only):  ")
OfsetMiddle=input("Enter Roter MIDDLE Offset (numbers only):  ")
OfsetRight=input("Enter Roter RIGHT Offset (numbers only):  ")
if input("whould you like to use plugbord (y/n): ") in ('y','Y'):
    plug= input("Enter the plugs (as followed : AB CD EF MUST BE CAPITELIZED): ")
    plug=plug.split(' ')
    dic_plug={}
    for res in plug:
        dic_plug[res[0]]=res[1]
        dic_plug[res[1]]=res[0]
M2=Machine(int(left),int(middle),int(right),int(OfsetLeft),int(OfsetMiddle),int(OfsetRight),int(setLeft),int(setMiddle),int(setRight),Plugboard(dic_plug))
M2.Encr()

