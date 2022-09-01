import csv
import re


def get_info(file_name: str) -> list:
    with open(file_name, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


def transpose(matrix: list) -> list:
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    return transposed


def phone(phone_list: list) -> None:
    for i, phone in enumerate(phone_list):
        search_pattern = r'(\+7|8)[\s(]*(\d{3})[)\s-]*(\d{3})-*(\d{2})-*(\d{2})[\s(]*(доб\.)*\s*(\d{4})*\)*'
        replace_pattern = r'+7(\2)\3-\4-\5 \6\7'
        new_phone = re.sub(search_pattern, replace_pattern, phone)
        phone_list[i] = new_phone.strip()


def lastname(transposed_contact_list: list) -> None:
    for i, lastname in enumerate(transposed_contact_list[0]):
        pattern = r'[а-яёА-ЯЁ]+'
        splitted = (re.findall(pattern, lastname))
        if len(splitted) == 2:
            transposed_contact_list[0][i] = splitted[0]
            transposed_contact_list[1][i] = splitted[1]
        elif len(splitted) == 3:
            transposed_contact_list[0][i] = splitted[0]
            transposed_contact_list[1][i] = splitted[1]
            transposed_contact_list[2][i] = splitted[2]
        else:
            pass


def firstname(transposed_contact_list: list) -> None:
    for i, firstname in enumerate(transposed_contact_list[1]):
        pattern = r'[а-яёА-ЯЁ]+'
        splitted = (re.findall(pattern, firstname))
        if len(splitted) == 2:
            transposed_contact_list[1][i] = splitted[0]
            transposed_contact_list[2][i] = splitted[1]


def doubled_contacts(contact_list: list) -> list:
    final_list = list()
    final_list.append(contact_list[0])
    del (contact_list[0])
    contact_list.sort()
    final_list.append(contact_list[0])
    for person in contact_list:
        if person[0] == final_list[-1][0] and person[1] == final_list[-1][1]:
            for i, parameter in enumerate(final_list[-1]):
                if not parameter:
                    final_list[-1][i] = person[i]
        else:
            final_list.append(person)
    return final_list


def save_info(file_name: str, contact_list: list) -> None:
    with open(file_name, "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contact_list)

#
if __name__ == '__main__':
    contacts_list = get_info("phonebook_raw.csv")
    transposed_list = transpose(contacts_list)
    phone(transposed_list[5])
    lastname(transposed_list)
    firstname(transposed_list)
    contact_list = transpose(transposed_list)
    ordered_contact_list = doubled_contacts(contact_list)
    save_info("phonebook.csv", ordered_contact_list)