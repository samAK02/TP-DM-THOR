# Algorithme 1||Cmax 
def main():

    n = -2
    while n<0:
        n = int(input("Veuillez entrer le nombre de taches: "))
        if (n<0):
            print("le nombre de tâches doit être positif")      
    C = []
    P = []
    S = []

    for i in range(n):
        P[i] = float(input("Veuillez entrer la durée de la tâche", i+1))
        while P[i] <= 0:
            print("La durée de la tâche doit être positive! ")
            P[i] = float(input("Veuillez entrer la durée de la tâche", i+1))

    S[0] = 0
    C[0] = S[0] + P[0]

    for i in range(n):
        S[i] = C[i-1]
        C[i] = S[i] + P[i]

    Cmax = C[n]



if __name__ == "__main__":
    main()