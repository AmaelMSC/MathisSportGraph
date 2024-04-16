import pandas as pd
import numpy as np

def format_string(s,i):
    ret = ""
    acc = 0
    for c in s:
        if acc >= i and c == " ":
            acc = 0
            ret += "\n"
        ret += c
        acc += 1
    ret = ret.replace("\n ", "\n")
    return ret

def average(T):
    return sum(T) / len(T)

def averages(data):
    return [average(T) for T in data]

def add_lists(L, d):
    for i in range(len(L)):
        if not pd.isna(d[i]):
            L[i] += d[i]

def retrive_data(sheet_name_custom):
    sheet = pd.read_excel("main.xlsx", sheet_name=sheet_name_custom, skiprows=[0])
    column_names = sheet.columns.tolist()[1:]
    categ_names = sheet[sheet.columns[0]].tolist()[1:]
    number_by_categ = {"Techniques OFF": 6, "Techniques DEF" : 6, "Athlétique" : 7, "Tactique" : 6, "Mentalité" : 8}
    starters = []

    numbers = list(number_by_categ.values())
    for i in range(1,len(numbers)+1):
        temp = 0
        for j in range(i):
            temp += numbers[j]
        starters.append(temp)
    for i in range(len(starters)):
        starters[i] += 2 + i

    big_data = {}

    tech_off_names = [format_string(e,10) for e in categ_names[2:starters[0]]]
    tech_def_names = [format_string(e,10) for e in categ_names[starters[0]+3:starters[1]+2]]
    athl_names = [format_string(e,16) for e in categ_names[starters[1]+5:starters[2]+4]]
    tact_names = [format_string(e,10) for e in categ_names[starters[2]+7: starters[3]+6]]
    ment_names = [format_string(e,16) for e in categ_names[starters[3]+9:]]
    names = [tech_off_names, tech_def_names, athl_names, tact_names, ment_names]


    pnumber = 0
    tech_off_averages = [0] * len(names[0])
    tech_def_averages = [0] * len(names[1])
    athl_averages = [0] * len(names[2])
    tact_averages = [0] * len(names[3])
    ment_averages = [0] * len(names[4])
    averages = [tech_off_averages, tech_def_averages, athl_averages, tact_averages, ment_averages]

    for colname in column_names:
        
        if colname.startswith("Unnamed"): continue
        pnumber += 1
        column = sheet[colname].tolist()[1:]

        tech_off_data = column[2:starters[0]]
        add_lists(tech_off_averages, tech_off_data)
        tech_def_data = column[starters[0]+3:starters[1]+2]
        add_lists(tech_def_averages, tech_def_data)
        athl_data = column[starters[1]+5:starters[2]+4]
        add_lists(athl_averages, athl_data)
        tact_data = column[starters[2]+7:starters[3]+6]
        add_lists(tact_averages, tact_data)
        ment_data = column[starters[3]+9:]
        add_lists(ment_averages, ment_data)

        big_data.update({colname:[tech_off_data, tech_def_data, athl_data, tact_data, ment_data]})


    averages_data = [[e / pnumber for e in data] for data in averages]

    return column_names, names, big_data, averages_data