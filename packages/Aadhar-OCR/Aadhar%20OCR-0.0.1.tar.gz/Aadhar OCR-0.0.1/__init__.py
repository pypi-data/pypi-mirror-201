import os
import os.path
import json
import sys
import pytesseract
import re
import csv
from PIL import Image
import spacy

def adharOcr(image_path):

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    name = None
    gender = None
    ayear = None
    uid = None
    yearline = []
    genline = []
    nameline = []
    text1 = []
    text2 = []
    genderStr = '(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$'
    lines = text

    #print(text)
    #Searching for Year of Birth

    dob_regex = r'\d{2}/\d{2}/\d{4}'
    dob_match = re.search(dob_regex, text)
    if dob_match:
        dob = dob_match.group()
        #print("DOB found:", dob)
    # else:
    #     print("DOB not found")

    #Searching for Gender

    gender_regex = r'[M|F]'
    gender_match = re.search(gender_regex, text)
    if gender_match:
        gender = gender_match.group()
    #     if gender == 'M':
    #         print("Gender: Male")
    #     elif gender == 'F':
    #         print("Gender: Female")
    # else:
    #     print("Gender not found")

    # Searching for Aadhar number
    clean_text = text.replace("_", " ")
    uid_regex = r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"
    uid_match = re.search(uid_regex, clean_text)
    if uid_match:
        uid = uid_match.group()
    #     print("UID: ", uid)
    # else:
    #     print("UID not found")

    #Searching for Name

    name_regex = r'[A-Z][a-z]+(?: [A-Z][a-z]+)*'

    match = re.search(name_regex, text)

    if match:
        name = match.group()
    #     print(f"Name found: {name}")
    # else:
    #     print("Name not found")
    # Making tuples of data

    data = {
        'gender': gender,
        'dob': dob,
        'aadhar': uid,
        'name':name
    }

    with open('aadhar_data.json', 'w') as outfile:
        json.dump(data, outfile)

    with open('aadhar_data.json', 'r') as file:
        data = json.load(file)
    print(data['name'])
    print("-------------------------------")
    print(data['aadhar'])
    print("-------------------------------")
    print(data['dob'])
    print("-------------------------------")
    print(data['gender'])
    print("-------------------------------")

