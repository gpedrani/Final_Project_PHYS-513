import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 


def main():
    
    #import all data
    files = ["L_6_cir_t_5", "L_6_cir_t_10", "L_6_cir_t_5",
             "L_8_cir_t_5", "L_8_cir_t_10", "L_8_cir_t_15",
             "L_10_cir_t_5", "L_10_cir_t_10", "L_10_cir_t_15"
             ]

    data = []
    for file in files:
        df = pd.read_csv(f"~/Documents/USC/PHYS-513/Final_Project/data/{file}.csv", sep=',') 
        data.append(df)
    
    fig, axs = plt.subplots(3,3) 
    #L=6 subplots 
    x = [i for i in range(1,6)]
    index = [0,1,2]
    for i in range(0,3):
        a = index[i]
        d = data[a]
        keys = d.keys()

        y1 = []
        y2 = []
        for j in keys:
            y1.append(np.complex128(d[j][0]))
            y2.append(np.complex128(d[j][1]))

        axs[0,i].plot(x, y1[1:], "+-", label='p = 1/6')
        axs[0,i].plot(x, y2[1:], "+-", label='p = 2/6')

    
    #L=8 subplots 
    x = [i for i in range(1,8)]
    index = [3,4,5]
    for i in range(0,3):
        a = index[i]
        d = data[a]
        keys = d.keys()

        y1 = []
        y2 = []
        y3 = []
        for j in keys:
            y1.append(np.complex128(d[j][0]))
            y2.append(np.complex128(d[j][1]))
            y3.append(np.complex128(d[j][2]))


        axs[1,i].plot(x, y1[1:], "+-", label='p = 1/8')
        axs[1,i].plot(x, y2[1:], "+-", label='p = 2/8')
        axs[1,i].plot(x, y3[1:], "+-", label='p = 3/8')

    #L=10 subplots 
    x = [i for i in range(1,10)]
    index = [6,7,8]
    for i in range(0,3):
        a = index[i]
        d = data[a]
        keys = d.keys()

        y1 = []
        y2 = []
        y3 = []
        y4 = []
        for j in keys:
            y1.append(np.complex128(d[j][0]))
            y2.append(np.complex128(d[j][1]))
            y3.append(np.complex128(d[j][2]))
            y4.append(np.complex128(d[j][3]))

        axs[2,i].plot(x, y1[1:], "+-", label='p = 1/10')
        axs[2,i].plot(x, y2[1:], "+-", label='p = 2/10')
        axs[2,i].plot(x, y3[1:], "+-", label='p = 3/10')
        axs[2,i].plot(x, y4[1:], "+-", label='p = 4/10')

    #set Titles
    fig.suptitle(r"Renyi 2nd Entropy Vs Subspace Size for Various Qubit Chains ($L$) and Gate Cycles ($t$) Combinations")
    axs[0,0].set_title(r'$L$=6, $t$=5')
    axs[0,1].set_title(r'$L$=6, $t$=10')
    axs[0,2].set_title(r'$L$=6, $t$=15')

    axs[1,0].set_title(r'$L$=8, $t$=5')
    axs[1,1].set_title(r'$L$=8, $t$=10')
    axs[1,2].set_title(r'$L$=8, $t$=15')

    axs[2,0].set_title(r'$L$=10, $t$=5')
    axs[2,1].set_title(r'$L$=10, $t$=10')
    axs[2,2].set_title(r'$L$=10, $t$=15')

    #Show Legeneds
    axs[0,0].legend()
    axs[0,1].legend()
    axs[0,2].legend()
    axs[1,0].legend()
    axs[1,1].legend()
    axs[1,2].legend()
    axs[2,0].legend()
    axs[2,1].legend()
    axs[2,2].legend()
     
    for ax in axs.flat:
        ax.set(ylabel=r"$S^2(A)$")
        ax.grid()
    
    axs[2,0].set(xlabel=r"$A$")
    axs[2,1].set(xlabel=r"$A$")
    axs[2,2].set(xlabel=r"$A$")

    #save fig
    #plt.savefig(f'./data/All_Entropies.png',dpi=1000)

    plt.show()

main()
