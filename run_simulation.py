from imports import *

def main(a,b,c):
    #initialize circuit parameters
    L = a  
    depth = b 
    p = c 
    subspaces = find_subspaces(L)

    #Construct backend once
    backend = AerSimulator(method='density_matrix')

    runs = {}
    for measurement_rate in p:
        print(f"Running loop: {measurement_rate}")
        #Contstruct Random Circuit of Fixed Length 
        qc = rand_real_circ2(L, measurement_rate, depth)

        #Save Density Matrix and run simulator
        qc.save_density_matrix()
        comp_qc = transpile(qc, backend)
        result = backend.run(comp_qc, shots=10000).result()
        rho = result.data()

        #Perform Diagonilzation and Renyi Entropy Calculations
        D = diagonalize(rho['density_matrix']) 

        sub_ents = {}
        for item in subspaces:
            reduc_rho = partial_trace(rho['density_matrix'], list(item))
            D = diagonalize(reduc_rho)
            sub_ents[f"{item}"] = [len(item), renyi(D, 2)]

        #Save current run to dictionary out of the loop
        runs[f"{measurement_rate}"] = sub_ents    
    #End of Measurement Loop---------------------------------------------

    new_ent = {}
    for key in runs.keys():
        a = runs[key]
        b = {}
        for i in range(0,L):
            running_ave = 0
            count = 0
            for pair in a.values():
                if pair[0] == i:
                    count += 1
                    if pair[1] < 50:
                        running_ave += pair[1]
        
            if count != 0:
                running_ave = running_ave/count
            if running_ave != 0: 
                b[i] = running_ave
        new_ent[key] = b 


    #Make Plots and CSV: 
    print("Making Figures and writing data to file")
    plt.figure()
    plt.title(f'Renyi Entropy vs SubSystem Size for Fixed $L = {L}, t={depth}$')
    plt.xlabel(r'$A$')
    plt.ylabel(r'$S_{A}^2 (\rho_{A})$')
    plt.grid()
    for key in new_ent.keys():
        run = new_ent[key]
        x , y = zip(*run.items())
        plt.plot(x, y, 'x-', label=f"p = {key}")
    plt.legend()
    plt.savefig(f'./data/L_{L}_cir_t_{depth}.png')
    plt.close() 

    
        
    df = pd.DataFrame.from_dict(new_ent, orient='index')
    df.to_csv(f"./data/L_{L}_cir_t_{depth}.csv")


def sim():
    
    Ls = [6,8,10]
    depths = [5,10,15]
    probs = {"6": [1/6, 2/6], 
             "8": [1/8,2/8, 3/8], 
             "10": [1/10, 2/10, 3/10, 4/10]
             }
    for length in Ls:
        for depth in depths:
            main(length, depth, probs[f"{length}"])

sim()

