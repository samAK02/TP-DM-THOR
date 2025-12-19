def spt1_lpt2(tasks):
 
    X = [t for t in tasks if t[1] <= t[2]]
    T_minus_X = [t for t in tasks if t[1] > t[2]]

    X_sorted = sorted(X, key=lambda t: t[1])
    T_minus_X_sorted = sorted(T_minus_X, key=lambda t: t[2], reverse=True)

    sequence = X_sorted + T_minus_X_sorted
    return sequence

def calcul_dates(sequence):
    n = len(sequence)
    
    # Structures de stockage
    t1 = [0] * n  # dates de début sur M1
    C1 = [0] * n  # dates de fin sur M1
    t2 = [0] * n  # dates de début sur M2
    C2 = [0] * n  # dates de fin sur M2

    # Initialisation pour la première tâche
    _, p11, p12 = sequence[0]
    t1[0] = 0
    C1[0] = p11
    t2[0] = C1[0]
    C2[0] = t2[0] + p12

    # Boucle principale
    for i in range(1, n):
        _, pi1, pi2 = sequence[i]

        t1[i] = C1[i - 1]
        C1[i] = t1[i] + pi1

        t2[i] = max(C1[i], C2[i - 1])
        C2[i] = t2[i] + pi2

    Cmax = C2[-1]

    return {
        "t1": t1,
        "C1": C1,
        "t2": t2,
        "C2": C2,
        "Cmax": Cmax
    }
###############################################################################################################################################################################
def fm_spt(tasks):
 
    return sorted(tasks, key=lambda t: sum(t[1]))

def calcul_dates_fm(sequence, m):
   
    n = len(sequence)

    # Dates de début et de fin
    t = [[0] * m for _ in range(n)]
    C = [[0] * m for _ in range(n)]

    for i in range(n):
        for k in range(m):
            if i == 0 and k == 0:
                t[i][k] = 0
            elif i == 0:
                t[i][k] = C[i][k - 1]
            elif k == 0:
                t[i][k] = C[i - 1][k]
            else:
                t[i][k] = max(C[i - 1][k], C[i][k - 1])

            C[i][k] = t[i][k] + sequence[i][1][k]

    Cmax = C[n - 1][m - 1]
    return t, C, Cmax

######################################################################################################################################################################################



def johnson_2machines(tasks):

    left = []
    right = []

    remaining = tasks.copy()

    while remaining:
        # Trouver la tâche avec le plus petit temps
        task = min(remaining, key=lambda t: min(t[1], t[2]))

        if task[1] <= task[2]:
            left.append(task)
        else:
            right.insert(0, task)

        remaining.remove(task)

    return left + right


def johnson_3machines(tasks):

    p1 = [t[1][0] for t in tasks]
    p2 = [t[1][1] for t in tasks]
    p3 = [t[1][2] for t in tasks]

    if not (min(p1) >= max(p2) or min(p3) >= max(p2)):
        raise ValueError(
            "Conditions de Johnson non vérifiées : "
            "min(p1) >= max(p2) ou min(p3) >= max(p2)"
        )

    # Réduction à 2 machines
    reduced_tasks = []
    for tid, times in tasks:
        p1p = times[0] + times[1]
        p2p = times[1] + times[2]
        reduced_tasks.append((tid, p1p, p2p))

    # Johnson classique
    sequence_2m = johnson_2machines(reduced_tasks)

    # Récupération des tâches originales dans le bon ordre
    seq_ids = [t[0] for t in sequence_2m]
    return [t for t in tasks if t[0] in seq_ids], seq_ids



def calcul_Cij(sequence):

    n = len(sequence)
    m = len(sequence[0][1])

    C = [[0] * m for _ in range(n)]

    # C11
    C[0][0] = sequence[0][1][0]

    # Première tâche, machines 2 à m
    for j in range(1, m):
        C[0][j] = C[0][j - 1] + sequence[0][1][j]

    # Première machine, tâches 2 à n
    for i in range(1, n):
        C[i][0] = C[i - 1][0] + sequence[i][1][0]

    # Cas général
    for i in range(1, n):
        for j in range(1, m):
            C[i][j] = max(C[i - 1][j], C[i][j - 1]) + sequence[i][1][j]

    Cmax = C[n - 1][m - 1]
    return C, Cmax


#################################################################################################################################################################


def calcul_LB1_LB2(tasks):
 
    n = len(tasks)
    m = len(tasks[0][1])

    # LB1 : max somme des durées par tâche
    LB1 = max(sum(times) for _, times in tasks)

    # LB2 : max somme des durées par machine
    LB2 = max(
        sum(tasks[i][1][j] for i in range(n))
        for j in range(m)
    )

    return LB1, LB2


def calcul_LB3(tasks):
 
    n = len(tasks)
    m = len(tasks[0][1])

    LB3_j = []

    for j in range(m):
        # Somme des durées sur la machine j
        sum_machine_j = sum(tasks[i][1][j] for i in range(n))

        # Partie gauche : machines 1 à j-1
        if j == 0:
            left_min = 0
        else:
            left_min = min(
                sum(tasks[i][1][k] for k in range(j))
                for i in range(n)
            )

        # Partie droite : machines j+1 à m
        if j == m - 1:
            right_min = 0
        else:
            right_min = min(
                sum(tasks[i][1][k] for k in range(j + 1, m))
                for i in range(n)
            )

        LB3_j.append(left_min + sum_machine_j + right_min)

    return max(LB3_j), LB3_j


##############################################################################################################################################################

def gupta_heuristic(tasks):

    sequence = []

    for tid, times in tasks:
        m = len(times)

        # Calcul de s_i
        if times[0] < times[m - 1]:
            s_i = 1
        else:
            s_i = -1

        # Calcul du dénominateur
        min_sum = min(times[k] + times[k + 1] for k in range(m - 1))

        # Calcul de e_i
        e_i = s_i / min_sum

        sequence.append((tid, times, e_i))

    # Tri décroissant selon e_i
    sequence.sort(key=lambda x: x[2], reverse=True)

    # Suppression de la clé e_i
    return [(tid, times) for tid, times, _ in sequence]


def calcul_Cij(sequence):

    n = len(sequence)
    m = len(sequence[0][1])

    C = [[0] * m for _ in range(n)]

    # C11
    C[0][0] = sequence[0][1][0]

    # Première tâche
    for j in range(1, m):
        C[0][j] = C[0][j - 1] + sequence[0][1][j]

    # Première machine
    for i in range(1, n):
        C[i][0] = C[i - 1][0] + sequence[i][1][0]

    # Cas général
    for i in range(1, n):
        for j in range(1, m):
            C[i][j] = max(C[i - 1][j], C[i][j - 1]) + sequence[i][1][j]

    Cmax = C[n - 1][m - 1]
    return C, Cmax


#############################################################################################################################################################################
def lapt_heuristic(tasks):

    remaining = tasks.copy()
    sequence = []

    while remaining:
        # Choisir la tâche avec le plus long temps sur l'autre machine (machine 2)
        task = max(remaining, key=lambda t: t[1][1])
        sequence.append(task)
        remaining.remove(task)

    return sequence



def calcul_Cij(sequence):

    n = len(sequence)
    m = 2

    C = [[0] * m for _ in range(n)]

    # C11
    C[0][0] = sequence[0][1][0]
    C[0][1] = C[0][0] + sequence[0][1][1]

    for i in range(1, n):
        # Machine 1
        C[i][0] = C[i - 1][0] + sequence[i][1][0]
        # Machine 2
        C[i][1] = max(C[i][0], C[i - 1][1]) + sequence[i][1][1]

    Cmax = C[n - 1][1]
    return C, Cmax


 ##############################################################################################################################################################################

def gard_algorithm(tasks):

    n = len(tasks)

    # Étape 1 : trouver p_kh = max{p_ij}
    max_time = -1
    k = -1
    h = -1  # machine indexée 0 ou 1

    for idx, (_, times) in enumerate(tasks):
        for j in range(2):
            if times[j] > max_time:
                max_time = times[j]
                k = idx
                h = j

    Tk = tasks[k]

    # Étape 2 : Tk est traité en premier
    sequence = [Tk]

    # Étape 3 : les autres tâches dans un ordre arbitraire (ici l'ordre initial)
    for i in range(n):
        if i != k:
            sequence.append(tasks[i])

    return sequence


def calcul_Cij(sequence):
    """
    Calcul des dates de fin Cij pour F2||Cmax
    """
    n = len(sequence)

    C = [[0, 0] for _ in range(n)]

    # Première tâche
    C[0][0] = sequence[0][1][0]
    C[0][1] = C[0][0] + sequence[0][1][1]

    for i in range(1, n):
        # Machine 1
        C[i][0] = C[i - 1][0] + sequence[i][1][0]
        # Machine 2
        C[i][1] = max(C[i][0], C[i - 1][1]) + sequence[i][1][1]

    Cmax = C[n - 1][1]
    return C, Cmax


##############################################################################################################################################################################

def mls_algorithm(tasks, sequences):

    n = len(tasks)
    m = len(sequences)

    # Dates de fin Cij
    C = {i: {j: 0 for j in range(m)} for i in range(n)}

    # Disponibilités
    machine_available = [0] * m
    task_available = [0] * n

    # Copie des séquences
    seq = {j: sequences[j][:] for j in range(m)}

    total_operations = n * m
    scheduled_operations = 0
    t = 0

    while scheduled_operations < total_operations:
        # Machines disponibles à l'instant t
        available_machines = [
            j for j in range(m)
            if machine_available[j] <= t and seq[j]
        ]

        if not available_machines:
            t = min(machine_available)
            continue

        # Première machine disponible
        j = min(available_machines)

        # Première tâche de la séquence
        i = seq[j].pop(0)

        # Ordonnancer le plus tôt possible
        start = max(machine_available[j], task_available[i])
        finish = start + tasks[i][j]

        C[i][j] = finish
        machine_available[j] = finish
        task_available[i] = finish

        scheduled_operations += 1
        t = min(machine_available)

    Cmax = max(C[i][j] for i in range(n) for j in range(m))
    return C, Cmax


def main():

    while True:
        print("\nChoisissez l'algorithme à exécuter :")
        print("1 - F2 || Cmax (SPT(1) - LPT(2))")
        print("2 - Fm || Cmax (SPT - Gonzalez & Sahni)")
        print("3 - F3 || Cmax (Johnson étendu)")
        print("4 - Heuristique de Gupta (Fm || perm || Cmax)")
        print("5 - Heuristique LAPT (F2 || Cmax)")
        print("6 - Heuristique GARD (F2 || Cmax)")
        print("7 - MLS (Multi List Scheduling)")
        print("8 - Bornes inférieures (LB1, LB2, LB3)")
        print("0 - Quitter")

        choix = input("\nVotre choix : ")

        # ========================================== QUITTER 
        if choix == "0":
            print("Fin du programme.")
            break

        # ========================================== F2 SPT-LPT 
        elif choix == "1":
            n = int(input("Nombre de tâches : "))
            tasks = []
            for i in range(n):
                p1 = int(input(f"T{i+1} - M1 : "))
                p2 = int(input(f"T{i+1} - M2 : "))
                tasks.append((f"T{i+1}", p1, p2))

            seq = spt1_lpt2(tasks)
            t1, C1, t2, C2, Cmax = calcul_dates(seq)

            print("\nSéquence :", " -> ".join(t[0] for t in seq))
            print("Cmax =", Cmax)

        # ========================================== Fm SPT 
        elif choix == "2":
            n = int(input("Nombre de tâches : "))
            m = int(input("Nombre de machines : "))
            tasks = []

            for i in range(n):
                times = [int(input(f"T{i+1} - M{j+1} : ")) for j in range(m)]
                tasks.append((f"T{i+1}", times))

            seq = fm_spt(tasks)
            C, Cmax = calcul_Cij(seq)

            print("\nSéquence :", " -> ".join(t[0] for t in seq))
            print("Cmax =", Cmax)

        # ========================================== JOHNSON 3 MACHINES
        elif choix == "3":
            n = int(input("Nombre de tâches : "))
            tasks = []

            for i in range(n):
                times = [int(input(f"T{i+1} - M{j+1} : ")) for j in range(3)]
                tasks.append((f"T{i+1}", times))

            try:
                seq, ids = johnson_3machines(tasks)
                C, Cmax = calcul_Cij(seq)
                print("\nSéquence :", " -> ".join(ids))
                print("Cmax =", Cmax)
            except ValueError as e:
                print("Erreur :", e)

        # ========================================== GUPTA 
        elif choix == "4":
            n = int(input("Nombre de tâches : "))
            m = int(input("Nombre de machines (>=3) : "))
            tasks = []

            for i in range(n):
                times = [int(input(f"T{i+1} - M{j+1} : ")) for j in range(m)]
                tasks.append((f"T{i+1}", times))

            seq = gupta_heuristic(tasks)
            C, Cmax = calcul_Cij(seq)

            print("\nSéquence :", " -> ".join(t[0] for t in seq))
            print("Cmax =", Cmax)

        # ========================================== LAPT 
        elif choix == "5":
            n = int(input("Nombre de tâches : "))
            tasks = []

            for i in range(n):
                p1 = int(input(f"T{i+1} - M1 : "))
                p2 = int(input(f"T{i+1} - M2 : "))
                tasks.append((f"T{i+1}", [p1, p2]))

            seq = lapt_heuristic(tasks)
            C, Cmax = calcul_Cij(seq)

            print("\nSéquence :", " -> ".join(t[0] for t in seq))
            print("Cmax =", Cmax)

        # ========================================== GARD 
        elif choix == "6":
            n = int(input("Nombre de tâches : "))
            tasks = []

            for i in range(n):
                p1 = int(input(f"T{i+1} - M1 : "))
                p2 = int(input(f"T{i+1} - M2 : "))
                tasks.append((f"T{i+1}", [p1, p2]))

            seq = gard_algorithm(tasks)
            C, Cmax = calcul_Cij(seq)

            print("\nSéquence :", " -> ".join(t[0] for t in seq))
            print("Cmax =", Cmax)

        # ========================================== MLS 
        elif choix == "7":
            n = int(input("Nombre de tâches : "))
            m = int(input("Nombre de machines : "))

            tasks = {}
            for i in range(n):
                tasks[i] = {}
                for j in range(m):
                    tasks[i][j] = int(input(f"T{i+1} - M{j+1} : "))

            sequences = {}
            for j in range(m):
                seq = input(f"Séquence M{j+1} (ex: 1 3 2) : ")
                sequences[j] = [int(x) - 1 for x in seq.split()]

            C, Cmax = mls_algorithm(tasks, sequences)
            print("Cmax =", Cmax)

        # ===================== BORNES =====================
        elif choix == "8":
            n = int(input("Nombre de tâches : "))
            m = int(input("Nombre de machines : "))
            tasks = []

            for i in range(n):
                times = [int(input(f"T{i+1} - M{j+1} : ")) for j in range(m)]
                tasks.append((f"T{i+1}", times))

            LB1, LB2 = calcul_LB1_LB2(tasks)
            LB3, _ = calcul_LB3(tasks)

            print("\nLB1 =", LB1)
            print("LB2 =", LB2)
            print("LB3 =", LB3)
            print("LB =", max(LB1, LB2, LB3))

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
