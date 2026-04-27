import random
subject=[[0,0,None],[0,0,None],[0,0,None],[0,0,None]]
n_subject=0

#Enrolment
def enrolment():
    global n_subject
    global subject
    if n_subject<4:        
        IDs=f'{random.randint(1,999):03}'
        print(f'\033[33mEnrolling in Subject-{IDs}\033[0m')
        subject[n_subject][0]=IDs
        subject[n_subject][1]=random.randint(25,100)
        if subject[n_subject][1]<50:
            subject[n_subject][2]='F'
        elif subject[n_subject][1]<65:
            subject[n_subject][2]='P'
        elif subject[n_subject][1]<75:
            subject[n_subject][2]='C'
        elif subject[n_subject][1]<85:
            subject[n_subject][2]='D'
        else:
            subject[n_subject][2]='HD'      

        n_subject+=1
        print(f'\033[33mYou are now enrolled in {n_subject} out of 4 Subjects\033[0m')
    else:
        print(f'\033[31mStudents are allowed to enrol in 4 subjects only\033[0m')
#Enrolment


#Withdraw
def withdraw():
    global n_subject
    global subject
    if n_subject==0:
        print(f'\033[31mThere are no subjects to withdraw\033[0m')
    else:
        rs=input('Remove subject by ID: ')
        ws=''
        for i in range(len(rs)):
            if rs[i].isdigit():
                ws+=rs[i]
        wsp=0
        for i in range(4):
            if subject[i][0]==ws:
                wsp=i
                print(f'\033[33mDroping subject {ws}\033[0m')
                if wsp<=n_subject-1: #rewriting matrix and number of enrolled subjects
                    subject[wsp][0]=subject[n_subject-1][0]; subject[n_subject-1][0]=0
                    subject[wsp][1]=subject[n_subject-1][1]; subject[n_subject-1][1]=0
                    subject[wsp][2]=subject[n_subject-1][2]; subject[n_subject-1][2]=None
                    n_subject-=1
                break
            elif i==3:
                print(f'\033[31mSubject does not exist in student enrolment\033[0m') 

#Withdraw
 

#Show Enrolment
def show_enrolment():
    global n_subject
    global subject
    if n_subject ==1:
        print(f'\033[33mShowing {n_subject} Subject\033[0m')
        print(f'Subject: {subject[0][0]} -- Mark= {subject[0][1]} -- Grade= {subject[0][2]}')
    elif n_subject >1:
        print(f'\033[33mShowing {n_subject} Subjects\033[0m')
        for i in range(n_subject):
            print(f'Subject: {subject[i][0]} -- Mark= {subject[i][1]} -- Grade= {subject[i][2]}')
    else:
        print(f'\033[31mStudent does NOT have any subject enrolled\033[0m')

#Show Enrolment
    

#Change password
def change_password():
    print(f'\033[33mUpdating password\033[0m')
    np=input('New password: ')
    npc=input('Confirm password: ')
    
    if np[0].isupper():
        cc=0; cn=0
        for i in range(len(np)):
            if np[i].isalpha():
                cc+=1
            elif np[i].isdigit():
                cn+=1
            else:
                print(f'\033[31mInvalid caracter in password. Use only letters and digits character - try again\033[0m')
                break            
        if cc>=5 and cn>=3 and cn+cc==len(np):
            if np==npc:
                print(f'\033[32mPassword has been successfully updated\033[0m')
            else:
                print(f'\033[31mPassword does not match - try again\033[0m')
        elif cn+cc==len(np):
            print(f'\033[31mPassword must contains at least five letters and three or more digits - try again\033[0m')
    else:
        print(f'\033[31mPassword must start with an upper-case character - try again\033[0m')     

#Change password

show_enrolment()
withdraw()
show_enrolment()