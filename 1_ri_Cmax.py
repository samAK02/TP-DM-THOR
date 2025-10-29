import random

def quick_sort(tab):
    if len(tab) <= 1:
        return tab
    pivot = random.choice(tab)
    gauche = [x for x in tab if x < pivot]
    milieu = [x for x in tab if x == pivot]
    droite = [x for x in tab if x > pivot]
    return quick_sort(gauche) + milieu + quick_sort(droite)



def merge_sort(tab):
    if len(tab) <= 1:
        return tab
    milieu = len(tab) // 2
    gauche = merge_sort(tab[:milieu])
    droite = merge_sort(tab[milieu:])
    return fusion(gauche, droite)


def fusion(gauche, droite):
    resultat = []
    i = j = 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    while i < len(gauche):
        resultat.append(gauche[i])
        i += 1
    while j < len(droite):
        resultat.append(droite[j])
        j += 1
    return resultat


def tri_adaptatif(tab):
    n = len(tab)
    if n <= 1:
        return tab

    cpt = 0
    for i in range(n - 1):
        if tab[i] > tab[i + 1]:
            cpt += 1

    ratio = cpt / (n - 1)

    if ratio == 0:
        print("Tableau déjà trié.")

        return tab
    elif ratio >= 0.4: 
        # valeur arbitraire mais juste utilisée dans un exemple
        print("Utilisation du QuickSort (tableau désordonné).")
        return quick_sort(tab)
    else:

        print("Utilisation du MergeSort (tableau peu désordonné).")
        return merge_sort(tab)



def main():
    n = -1
    while n <= 0:
        n = int(input("Veuillez entrer le nombre de tâches : "))
        if n <= 0:
            print("Le nombre de tâches doit être positif.")

    r = []
    P = []
    S = []
    C = []

    for i in range(n):
        ri = float(input(f"Date de disponibilité de la tâche {i + 1} : "))
        while ri < 0:
            print("La date de disponibilité doit être positive.")
            ri = float(input(f"Date de disponibilité de la tâche {i + 1} : "))

        Pi = float(input(f"Durée de la tâche {i + 1} : "))
        while Pi <= 0:
            print("La durée de la tâche doit être positive.")
            Pi = float(input(f"Durée de la tâche {i + 1} : "))

        r.append(ri)
        P.append(Pi)

    r_prime = []
    for i in range(len(r)):
        r_prime.append(r[i])


    r_trie = tri_adaptatif(r_prime)

    
    taches = list(zip(r, P))
    taches_triees = sorted(taches, key=lambda x: r_trie.index(x[0]))
    r = [x[0] for x in taches_triees]
    P = [x[1] for x in taches_triees]

    
    S.append(r[0])
    C.append(S[0] + P[0])
    

    for i in range(1, n):
        S.append(max(C[i - 1], r[i]))
        C.append(S[i] + P[i])

    Cmax = C[-1]

    print("la durée max est de: ", Cmax)


if __name__ == "__main__":
    main()
