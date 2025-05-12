from imports import *

def main(a,b,c):
    #initialize circuit parameters
    L = a  
    depths = b 
    p = c [0]
    subspaces = find_subspaces(L)

    #Construct backend once
    backend = AerSimulator(method='density_matrix')

    runs = {}
    for depth in depths:
        print(f"Running loop, depth: {depth}")
        #Contstruct Random Circuit of Fixed Length 
        qc = rand_real_circ3(L, p, depth)

        #Save Density Matrix and run simulator
        qc.save_density_matrix()
        comp_qc = transpile(qc, backend)
        result = backend.run(comp_qc, shots=1000).result()
        rho = result.data()

        #Perform Diagonilzation and Renyi Entropy Calculations
        D = diagonalize(rho['density_matrix']) 
        correction = renyi(D,2)

        sub_ents = {}
        for item in subspaces:
            reduc_rho = partial_trace(rho['density_matrix'], list(item))
            D = diagonalize(reduc_rho)
            corrected_ent = renyi(D, 2) - correction
            sub_ents[f"{item}"] = [len(item), corrected_ent]

        #Save current run to dictionary out of the loop
        runs[f"{depth}"] = sub_ents    
    #End of Depth Loop---------------------------------------------

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
    plt.title(f'Renyi Entropy vs SubSystem Size for Fixed $L = {L}, p={p}$')
    plt.xlabel(r'$A$')
    plt.ylabel(r'$S_{A}^2 (\rho_{A})$')
    plt.grid()
    for key in new_ent.keys():
        run = new_ent[key]
        x , y = zip(*run.items())
        plt.plot(x, y, 'x-', label=f"Depth = {key}")
    plt.legend()
    plt.savefig(f'./data/L_{L}_p_{p}_5.png')
    plt.close() 

    
        
    df = pd.DataFrame.from_dict(new_ent, orient='index')
    df.to_csv(f"./data/L_{L}_p_{p}_5.csv")


def sim():
    
    Ls = 8
    depths = [1,2,3,4,5,6,7]
    probs = {"8": [2/8]}
    main(Ls, depths, probs[f"{Ls}"])

sim()
