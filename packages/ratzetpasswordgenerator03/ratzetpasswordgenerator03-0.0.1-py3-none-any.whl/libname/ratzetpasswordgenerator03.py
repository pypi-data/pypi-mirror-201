# Approach
# Password contains the below
# atleast 1 uppercase letters from A to Z,
# atleast 1 lowercase letters from a to z,
# atleast 1 digits from 0 to 9,
# atleast 1 special character such as !, ?, “, # etc.
# passsword length should be atleast 8 characters

# importing libraries
import random


class PasswordGenerator:
    def __init__(self,n):
        self.n=n

    def passwordgenerator(self):
        #creating different list for characters, digits and special characters that will be part of the password generated.
        uppercase=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        lowercase=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        digits=['0','1','2','3','4','5','6','7','8','9']
        special=["!", "?", "#", "@","$","%"]
        all_characters=uppercase+lowercase+digits+special
        password=[]


        #n=int(input("Enter the number of characters in the password or the length of the passsword. Should be atleast 8 \n"))

        if n<8:
            print("Please enter the password length of greater than 8")
            
        else:
            password=random.choice(uppercase)+random.choice(lowercase)+random.choice(digits)+random.choice(special)
            password1=""
            for i in range(n-4):
                password1=password1+random.choice(all_characters)
            
            final_password=password+password1

        return(final_password)
        #print(f"The random password generated is : {final_password}")

#def main():
#   n=int(input("Enter the number of characters in the password or the length of the passsword. Should be atleast 8 \n"))
#    PG=PasswordGenerator(n)
 #   PG.passwordgenerator()


if __name__ == '__main__':
    n=int(input("Enter the number of characters in the password or the length of the passsword. Should be atleast 8 \n"))
    PG=PasswordGenerator(n)
    final_password=PG.passwordgenerator()
    print(f"The random password generated is : {final_password}")

