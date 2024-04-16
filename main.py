import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import numpy as np
import data
import radar_facto as radfac


def init(sheet_name_custom):
    column_names, names, big_data, averages_data = data.retrive_data(sheet_name_custom)
    for name in column_names:
        make_one(name, names, big_data, sheet_name_custom, averages_data)

def data_gen(pname, names, big_data):
    #names = [tech_off_names, tech_def_names, athl_names, tact_names, ment_names]
    data = big_data[pname]
        
    return zip(names, data)

def average(T):
    return sum(T) / len(T)

def averages(data):
    return [average(T) for T in data]

def make_one(pname, names, big_data, sheet_name, averages_data):
    gen = data_gen(pname, names, big_data)
    titles = ["Techniques OFF", "Techniques DEF", "Athlétique", "Tactique", "Mentalité"]

    fig, axs = plt.subplots(figsize=(10,10), nrows=3, ncols=2, subplot_kw=dict(projection="polar"))
    fig.subplots_adjust(wspace=0.50, hspace=0.40, top=0.85, bottom=0.05)
    fig.text(0.5, 0.68, f'Statistiques de\n{pname}',
                horizontalalignment='center', color='black', weight='bold',
                size='x-large')
    fig.tight_layout()
    row = 0
    col = 0

    for title, (names, data), average in zip(titles, gen, averages_data):
        N = len(names)
        theta = radfac.radar_factory(N, frame='polygon')

        names.append(names[0])
        data.append(data[0])
        average.append(average[0])
        theta = np.concatenate((theta, [theta[0]]))

        axs[row,col].set_ylim([0,20])
        axs[row,col].plot(theta, data, color='b')
        axs[row,col].set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                        horizontalalignment='center', verticalalignment='center')
        axs[row,col].set_thetagrids(theta * 180/np.pi, names)
        axs[row,col].xaxis.set_tick_params(pad=20)
        axs[row,col].fill(theta, data, facecolor='b', alpha=0.25, label='_nolegend_')
        axs[row, col].fill(theta, average, facecolor='r', alpha = 0.50, label='_nolegend_')

        col += 1
        if col == 2:
            row += 1
            col = 0
        
        names.pop()
        data.pop()
        average.pop()

    theta = radfac.radar_factory(len(titles), frame='polygon')
    data = big_data[pname]
    titles.append(titles[0])
    data.append(data[0])
    theta = np.concatenate((theta, [theta[0]]))
    axs[2,1].set_ylim([0,20])
    axs[2,1].plot(theta, averages(data), color = 'r')
    axs[2,1].set_title("Moyennes", weight='bold', size='medium', position=(0.5, 1.1),
                        horizontalalignment='center', verticalalignment='center')
    axs[2,1].set_thetagrids(theta * 180/np.pi, titles)
    axs[2,1].xaxis.set_tick_params(pad=20)
    axs[2,1].fill(theta, averages(data), facecolor='r', alpha=0.25, label='_nolegend_')

    plt.subplots_adjust(hspace=0.7)
    plt.savefig(f"Joueurs/{sheet_name}/{pname}.pdf", format="pdf", bbox_inches="tight")
    plt.close()

def verif_repertory_exists(repertory):
    chemin_du_repertoire = f"Joueurs/{repertory}"
    if not os.path.exists(chemin_du_repertoire):
        os.makedirs(chemin_du_repertoire)
        print(f"Le répertoire '{chemin_du_repertoire}' a été créé.")
    else:
        print(f"Le répertoire '{chemin_du_repertoire}' existe déjà.")


if __name__ == '__main__':
    if not os.path.exists("Joueurs"): os.makedirs("Joueurs")
    if sys.argv[1] == "all":
        for sheet_name in pd.ExcelFile("main.xlsx").sheet_names:
            verif_repertory_exists(sheet_name)
            init(sheet_name)
    else:
        verif_repertory_exists(sys.argv[1])
        init(sys.argv[1])
