import re
"""
Консольна програма записує список телефонних номерів у файл, читає файл весь або видає номер по імені,
також можливо змінити номер на новий, або повністю видалити запис. Команда "help" показує всі команди на які реагує програма.
Ім'я може складатись з одного або двох слів (Латиниця або Кирилиця). Номер- в будь якому форматі
"""
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW="\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"

def list_add(member_str):
    member=dict()
    print(member_str)
    members_match=re.match(r"(\D)+ (\b\D\b)*",member_str)
    try:
        print(members_match.group())
        member["name"]=members_match.group().strip()
        member["tel"] = member_str.lstrip(members_match.group()).strip()
    except AttributeError:
        print("неправильна команда аdd, нaберіть help для справки")
    return member
def list_change(member_str):
    result=dict()
    members_match=re.match(r"(\D)+ (\b\D\b)*",member_str)
    try:
        sel_member=members_match.group().strip()
        new_tel=member_str.lstrip(members_match.group()).strip()
        for member in list_members:
            if member["name"].lower()==sel_member.lower():
               member["tel"]=new_tel
               return member
        print(f"{members_match.group().strip()}  у Вашому списку нема")
    except AttributeError:
        print("неправильна команда change, нaберіть help для справки")

    return  result
def search_phone(member):
    try:
        tel_mem = list(filter(lambda m: str(m["name"]).lower() == member.strip().lower(), list_members))
        if len(tel_mem) > 0:
            print(f'tel of {member.strip()} is {tel_mem[0]["tel"]}')
        else:
            print(f"{member.strip()} не знайдено у Вашому списку")
    except IndexError:
        print("неправильна команда phone, нaберіть help для справки")

def delete_phone(member):
    print(member)
    try:
        n=0
        yes=True

        for m in list_members:
            if m["name"].lower()== member.lower():
                print(m["name"])
                m_del=list_members.pop(n)
                print(f'tel of {m_del["name"]} was deleted')
                yes=False
                break
            n+=1
        if yes:
            print(f"{member}  не знайдено у Вашому списку")
    except IndexError:
        print("неправильна команда phone, нaберіть help для справки")


def help():
    print(f' List of comand:\n {YELLOW}add Name [Name2] Telephone {BLUE}- added member to list\n'
          f'{YELLOW} Hello {BLUE}- Hello\n'
          f'{YELLOW} add{RESET} Name [Name2] Number of Tel{BLUE}- add member to list\n'
          f'{YELLOW} change {RESET}Name [Name2] Number of Tel{BLUE}- change number of tel of member in list\n'
          f'{YELLOW} delete {RESET}Name [Name2] {BLUE}- delete number of tel and member from list\n'
          f'{YELLOW} phone {RESET}Name [Name2]{BLUE}- shows the phone number of member\n'
          f'{YELLOW} show all {BLUE}- shows all list\n'
          f'{YELLOW} help {BLUE}- help\n'
          f'{YELLOW} exit or close or good bye {BLUE}- exit from program\n{RESET}')
def input_error(func):
    def inner():
       try:
          result=func()
          return result
       except Exception as ex:
          print(f"{RED}помилка - {YELLOW}{ex}- зверніться до розробника")
         # print(f'result - {result}')
    return inner
@input_error
def main():
    bye=("good bye", "close", "exit")
    while True:
       data = input(">")
       if data.lower()=="hello":
           print("Hello! How can I help you?")
           continue
       elif data.lower() in bye:
           print("Good bye!")
           with open(path_phone,"w+",encoding='utf-8') as phone_file:
               for mem in list_members:
                   phone_file.write(mem["name"]+', '+ mem["tel"]+'\n')
           break
       elif data[:3].lower() == "add":
           mem_add=list_add(data[3:].strip())
           if (mem_add):
               list_members.append(mem_add)
               print(f'added new entry in the phone book: {mem_add["name"]} - {mem_add["tel"]}')
       elif data[:6].lower() == "change":
           mem_change=list_change(data[6:].strip())
           if len(mem_change)>0:
               print(f'for {mem_change["name"]} phone number was changed to {mem_change["tel"]}')
       elif data[:5].lower() == "phone":
           search_phone(data[5:].strip())
       elif data[:8].lower() == "show all":
           print("list is: ")
           for mem in list_members:
               print(f'{mem["name"]} - {mem["tel"]}')
       elif data[:6].lower()=="delete":
           print("--------")
           delete_phone(data[6:].strip())

       elif data[:4].lower() == "help":
           help()
       else:
          print(f'{RED}"{data}"  is unknown command{RESET}')
          help()




#main()
if __name__ == "__main__":
   path_phone='phone_list.txt'
   list_members=[]
   try:
       with open(path_phone, "r", encoding="UTF-8") as phone_file:
           while True:
               line=phone_file.readline()
               if not line:
                   break
               member=dict()
               line1 = line.split(',')
               member["name"]=line1[0].strip()
               member["tel"] = line1[1][:len(line1[1])-1].strip()
               list_members.append(member)
           #print(list_members)
   except FileNotFoundError:
       None
   main()

