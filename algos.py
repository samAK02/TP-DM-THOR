# Algorithme 1||Cmax 
def main():

    n = -2
    while n < 0:
        n = int(input("Veuillez entrer le nombre de tâches : "))
        if n < 0:
            print("le nombre de tâches doit être positif")

    
    C = []
    P = []
    S = []

    for i in range(n):
        
        Pi = float(input(f"Veuillez entrer la durée de la tâche {i + 1} : "))
        while Pi <= 0:
            print("la durée de la tâche doit être positive !")
            Pi = float(input(f"Veuillez entrer la durée de la tâche {i + 1} : "))
        P.append(Pi)

    S.append(0)
    C.append(S[0] + P[0])

    for i in range(1, n):
        S.append(C[i - 1])
        C.append(S[i] + P[i])

    Cmax = C[n - 1]

    print("la durée maximale du projet est de :", Cmax)


if __name__ == "__main__":
    main()

