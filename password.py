import string
import random
import os

desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop") #Kullanıcının masaüstü dizinine giden yolu saklar.
passwords_directory = os.path.join(desktop_directory, "passwords") #Masaüstü yoluna "passwords" adında klasör ekler.
os.makedirs(passwords_directory, exist_ok=True) #Passwords_directory dizini oluşturulur. 2.parametre, belirtilen dizin zaten varsa hata vermemesini sağlar.
password_file = os.path.join(passwords_directory, "passwords.txt") #Passwords klasörüne "passwords.txt" dosyasını ekler.

if not os.path.exists(password_file): # "password_file" dosyasının olup olmadığını konrtol eder
    print("File is creating.")
    with open(password_file, "w") as file:
        pass  # Boş dosya oluşturur.

def add_password(site,password,passwords): # passwords adlı dictionary'e ekleme yapar.
    passwords[site] = password
    print(f"Password for {site} added!")
    print("\n")

    with open(password_file,"a") as file: # password_file adlı dosyayı ekeleme modunda açar.
        file.write(f"{site} : {password} \n")

def view_passwords(passwords):
    for site, password in passwords.items():
        print(f"{site} : {password}")


def delete_password(passwords):
    site = input("Enter the site name to delete : ")
    if site.upper() in passwords: # site isminin küçük ya da büyük harfle yazılmasını önemsiz kılar.
        del passwords[site] # site ve şifreyi dictionary'den siler.
        print(f"password for {site} deleted.")
    else:
        print("Site not found")

    with open(password_file,"w") as file: # dosyayı dictionary'e göre günceller.
        for site, password in passwords.items():
            file.write(f"{site} : {password}\n")

def update_password(passwords):
    site = input("please enter the site to update it's password :")

    while True:
        if site in passwords:
            choice = input("1. Generate new password.\n2. I have password, just add.\nChoice : ")
            choice = int(choice)
            if choice == 1:
                num_letters = get_valid_number("How many letters do you want in the password? : ")
                num_digits = get_valid_number("How many digits do you want in the password? : ")
                num_punctuation = get_valid_number("How many punctuation characters do you want in the password? : ")
                while True:
                    password = generate_password(num_letters, num_digits, num_punctuation)
                    print(f"password : {password}")
                    is_okey = input("Do you like this password?(Y:Yes , N:No)")
                    if is_okey.upper() == "Y": # Girilen Y harfinin küçük ya da büyük olmasını önemsizleştirir.
                        passwords[site] = password
                        print("UPDATED PASSWORD!!")
                        break
                    elif is_okey.upper() == "N": # Girilen N harfinin küçük ya da büyük olmasını önemsizleştirir.
                        continue
                with open(password_file, "w") as file: # password_file adlı soyayı yazma modunda açar. Passwords adlı disctionary'e göre günceller.
                    for site, password in passwords.items():
                        file.write(f"{site} : {password}\n")
                break
            elif choice == 2:
                password = input("please enter your password (BE CAREFUL FOR UPPER LOWER CASE) : ")
                passwords[site] = password
                print("UPDATED PASSWORD!!")
                with open(password_file, "w") as file:
                    for site, password in passwords.items():
                        file.write(f"{site} : {password}\n")
                break
        else:
            print("The site to update password could not be found")
            break

def generate_password( num_letters, num_digits, num_punctuation):
    letters = string.ascii_letters
    digits = string.digits
    punctuation = string.punctuation

    password = []
    password.extend(random.choice(letters) for _ in range(num_letters)) #kullanıcıdan alınan sayıda karakteri seçer ve "password"e ekler.
    password.extend(random.choice(digits) for _ in range(num_digits))
    password.extend(random.choice(punctuation) for _ in range(num_punctuation))

    random.shuffle(password) # Listenin içindeki elemanları karıştırır.
    return ''.join(password) #Listenin elemanlarını aralarında boşluk kalmayacak şekilde birleştirir.


def found_site(passwords, input_site): # Girilen site adı dictonary içinde varsa 1 değerini döndürür.(büyük küçük harf önemsiz)     bool_found = 0
    for site in passwords:
        if site.upper() == input_site.upper():
            bool_found = 1
    return bool_found

def update_dictionary(): # dosya içeriği okunarak "passwords" adlı dictionarye eklenir.
    passwords = {}
    with open(password_file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                site, password = line.split(" : ")
                passwords[site] = password
        return passwords

def get_valid_number(number): # Kullanıcıyı pozitif tam sayı girmeye zorlar.
    while True:
        try:
            value = int(input(number))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def main():
    passwords = update_dictionary()
    while True:
        print("\n")
        print("1. Add Password")
        print("2. View Password")
        print("3. Delete Password")
        print("4. Update Password")
        print("5. Exit")
        print("\n")
        choice1 = input("YOUR CHOİCE : ")
        print("\n")
        choice1 = int(choice1)
        if choice1 == 1:
            while True:
                site = input("Please enter the site name : ")
                print("\n")
                if found_site(passwords, site) == 0:
                    choice2 = int(input("1. Generate new password.\n2. I have password, just add.\nYour Choice : "))
                    print("\n")
                    if choice2 == 1:
                        while True:
                            num_letters = get_valid_number("How many letters do you want in the password? : ")
                            num_digits = get_valid_number("How many digits do you want in the password? : ")
                            num_punctuation = get_valid_number("How many punctuation characters do you want in the password? : ")
                            while True:
                                password = generate_password(num_letters, num_digits, num_punctuation)
                                print(f"password : {password}")
                                is_okey = input("Do you like this password?(Y:Yes , N:No)")
                                if is_okey.upper() == "Y":
                                    add_password(site,password,passwords)
                                    break
                                elif is_okey.upper() == "N":
                                    continue
                            break
                    elif choice2 == 2:
                        password =  input("Please enter the password : ")
                        add_password(site, password,passwords)
                        break
                    else :
                        print("Please enter valid choice.")
                else :
                    print("YOU HAVE ALLREADY PASSWORD FOR THİS SİTE!! ")
                    print("\n")
                    break
                break
        elif choice1 == 2:
            view_passwords(passwords)
            break
        elif choice1 == 3:
            delete_password(passwords)
        elif choice1 == 4:
            update_password(passwords)
        elif choice1 == 5:
            break
        else:
            print("PLEASE ENTER VALİD CHOİCE!!!")
if __name__ == "__main__":
    main()