import heapq

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def calcul_Cmax_star(p, m):
    return max(max(p), sum(p) / m)

def ordonnancement_preemptif(p, m):
    Cmax_star = calcul_Cmax_star(p, m)

    i = 0
    j = 0
    t = 0

    machines = [[] for _ in range(m)]
    remaining = p.copy()

    while i < len(p):
        if j >= m:
            break

        if t + remaining[i] < Cmax_star:
            machines[j].append((i+1, t, t + remaining[i]))
            t += remaining[i]
            i += 1

        elif t + remaining[i] == Cmax_star:
            machines[j].append((i+1, t, Cmax_star))
            t = 0
            j += 1
            i += 1

        else:
            available = Cmax_star - t
            machines[j].append((i+1, t, Cmax_star))
            remaining[i] -= available
            t = 0
            j += 1

    return machines


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ordonnancement_P_C(p, m):
    tasks = sorted([(p[i], i+1) for i in range(len(p))])
    heap = [(0, k) for k in range(m)]
    heapq.heapify(heap)

    machines = [[] for _ in range(m)]

    for duration, task_num in tasks:
        end_time, machine_index = heapq.heappop(heap)

        start = end_time
        finish = start + duration

        machines[machine_index].append((task_num, start, finish))

        heapq.heappush(heap, (finish, machine_index))

    return machines



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ordonnancement_P_ri_Lmax(r, d, m):
    tasks = list(range(len(r)))
    remaining = set(tasks)

    machines = [[] for _ in range(m)]
    C = [-1] * len(r)

    t = min(r)

    while remaining:
        available = {i for i in remaining if r[i] <= t}
        k = 0

        while available and remaining:
            i = min(available, key=lambda x: d[x])

            machines[k].append((i+1, t, t+1))
            C[i] = t + 1

            available.remove(i)
            remaining.remove(i)

            if k < m - 1:
                k += 1
            else:
                k = 0
                t += 1
                available = {j for j in remaining if r[j] <= t}

        if not available and remaining:
            t = min(r[j] for j in remaining)

    Lmax = max(C[i] - d[i] for i in tasks)
    return machines, Lmax


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ordonnancement_P_Uw(d, w, m):
    n = len(d)
    tasks = list(range(n))
    tasks_sorted = sorted(tasks, key=lambda i: d[i])

    scheduled = []
    machines = [[] for _ in range(m)]
    placement = {}

    t = 0
    k = 0

    for i in tasks_sorted:
        if t + 1 > d[i] and scheduled and -scheduled[0][0] < w[i]:
            _, j = heapq.heappop(scheduled)

            for machine in machines:
                for entry in machine:
                    if entry[0] == j+1:
                        machine.remove(entry)
                        break

            start, end = placement[j]
            machines[k].append((i+1, start, end))
            placement[i] = (start, end)
            del placement[j]

            heapq.heappush(scheduled, (-w[i], i))

        else:
            machines[k].append((i+1, t, t+1))
            placement[i] = (t, t+1)
            heapq.heappush(scheduled, (-w[i], i))

        if k < m - 1:
            k += 1
        else:
            k = 0
            t += 1

    late_tasks = []
    for i in placement:
        _, end = placement[i]
        if end > d[i]:
            late_tasks.append(i+1)

    return machines, late_tasks



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ordonnancement_P_Uw_parallel(p, d, w, m):
    n = len(p)
    tasks = list(range(n))

    tasks_sorted = sorted(tasks, key=lambda i: d[i] / w[i])

    machines = [[] for _ in range(m)]
    machine_end = [0] * m
    placement = {}
    scheduled = []

    for i in tasks_sorted:
        k = min(range(m), key=lambda x: machine_end[x])
        t = machine_end[k]

        if t + p[i] > d[i]:
            if scheduled:
                ratio_j, j = heapq.heappop(scheduled)

                if ratio_j < (p[i] / d[i]):
                    mach_j, start_j, end_j = placement[j]
                    for entry in machines[mach_j]:
                        if entry[0] == j+1:
                            machines[mach_j].remove(entry)
                            break

                    machines[mach_j].append((i+1, start_j, start_j + p[i]))
                    placement[i] = (mach_j, start_j, start_j + p[i])
                    machine_end[mach_j] = max(machine_end[mach_j],
                                              start_j + p[i])

                    del placement[j]
                    heapq.heappush(scheduled, (p[i]/d[i], i))
                    continue
                else:
                    heapq.heappush(scheduled, (ratio_j, j))

        start = t
        end = t + p[i]
        machines[k].append((i+1, start, end))
        placement[i] = (k, start, end)
        machine_end[k] = end
        heapq.heappush(scheduled, (p[i] / d[i], i))

    late_tasks = [i+1 for i in placement if placement[i][2] > d[i]]
    return machines, late_tasks


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def saisir_liste_entiers(n, nom):

    liste = []
    for i in range(1, n+1):
        while True:
            try:
                val = int(input(f"{nom} de la tâche {i} : ").strip())
                liste.append(val)
                break
            except ValueError:
                print("Veuillez entrer un entier valide.")
    return liste

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main():
    print("Programme d'ordonnancement — menu")

    while True:
        print("\n--- Menu ---")
        print("1 - P | pmtn | Cmax")
        print("2 - P || C_barre ")
        print("3 - P | p_i = 1 , r_i | Lmax")
        print("4 - P | p_i = 1 | U_w")
        print("5 - P || U_w")
        print("0 - Quitter")

        try:
            choix = int(input("Votre choix : ").strip())
        except ValueError:
            print("Choix invalide.")
            continue

        if choix == 0:
            print("Au revoir.")
            break

        try:
         
            n = int(input("Nombre de tâches : ").strip())
            if n <= 0:
                print("Le nombre de tâches doit être positif.")
                continue

            m = int(input("Nombre de machines : ").strip())
            if m <= 0:
                print("Le nombre de machines doit être positif.")
                continue

            #choix 1 : P | pmtn | Cmax
            if choix == 1:
                print("\nSaisie des durées p_i :")
                p = saisir_liste_entiers(n, "durée p")
                machines = ordonnancement_preemptif(p, m)

                print("\nRésultat :")
                for k, mach in enumerate(machines):
                    print(f"Machine {k+1}: {mach}")

            #choix 2 : P || C_barre
            elif choix == 2:
                print("\nSaisie des durées p_i :")
                p = saisir_liste_entiers(n, "durée p")
                machines = ordonnancement_P_C(p, m)

                print("\nRésultat :")
                for k, mach in enumerate(machines):
                    print(f"Machine {k+1}: {mach}")

            #choix 3 : P | pᵢ = 1, rᵢ | Lmax
            elif choix == 3:
                print("\nToutes les tâches ont p_i = 1")
                r = saisir_liste_entiers(n, "date de disponibilité r")
                d = saisir_liste_entiers(n, "date échue d")
                machines, Lmax = ordonnancement_P_ri_Lmax(r, d, m)

                print("\nRésultat :")
                for k, mach in enumerate(machines):
                    print(f"Machine {k+1}: {mach}")
                print("\nLmax =", Lmax)

            #  choix 4 : P | p_i = 1 | U_w
            elif choix == 4:
                print("\nToutes les tâches ont p_i = 1")
                d = saisir_liste_entiers(n, "date échue d")
                w = saisir_liste_entiers(n, "poids w")
                machines, late = ordonnancement_P_Uw(d, w, m)

                print("\nRésultat :")
                for k, mach in enumerate(machines):
                    print(f"Machine {k+1}: {mach}")
                print("Tâches en retard :", late)

            #choix 5 : P || U_w
            elif choix == 5:
                print("\nSaisie des durées p_i :")
                p = saisir_liste_entiers(n, "durée p")
                d = saisir_liste_entiers(n, "date échue d")
                w = saisir_liste_entiers(n, "poids w")

                machines, late = ordonnancement_P_Uw_parallel(p, d, w, m)

                print("\nRésultat :")
                for k, mach in enumerate(machines):
                    print(f"Machine {k+1}: {mach}")
                print("Tâches en retard :", late)

            else:
                print("Choix invalide.")

        except Exception as e:
            print("Erreur :", e)



if __name__ == "__main__":
    main()
