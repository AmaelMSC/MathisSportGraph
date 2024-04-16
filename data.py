import pandas as pd

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

    for colname in column_names:
        column = sheet[colname].tolist()[1:]
        
        tech_off_names = [format_string(e,10) for e in categ_names[2:starters[0]]]
        tech_off_data = column[2:starters[0]]
        tech_def_names = [format_string(e,10) for e in categ_names[starters[0]+3:starters[1]+2]]
        tech_def_data = column[starters[0]+3:starters[1]+2]
        athl_names = [format_string(e,16) for e in categ_names[starters[1]+5:starters[2]+4]]
        athl_data = column[starters[1]+5:starters[2]+4]
        tact_names = [format_string(e,10) for e in categ_names[starters[2]+7: starters[3]+6]]
        tact_data = column[starters[2]+7:starters[3]+6]
        ment_names = [format_string(e,16) for e in categ_names[starters[3]+9:]]
        ment_data = column[starters[3]+9:]

        big_data.update({colname:[tech_off_data, tech_def_data, athl_data, tact_data, ment_data]})

    names = [tech_off_names, tech_def_names, athl_names, tact_names, ment_names]

    averages_data = []

    return column_names, names, big_data, averages_data