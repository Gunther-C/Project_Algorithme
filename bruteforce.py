from rich.console import Console
from rich.table import Table
from itertools import combinations
import csv
import time

force_brute = []

try:
    with open("data_csv/force_brute.csv", "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            force_brute.append(line)

except IOError as er:
    print("Erreur lors de l'ouverture du fichier :", er)
except UnicodeEncodeError as err:
    print("Erreur D'encodage :", err)


start = time.time()
rotate = 0

possibility = []
possibilities = []

for i in range(1, len(force_brute) + 1):

    for this in combinations(force_brute, i):
        this = list(this)
        spend: int = 0
        profit_all: float = 0.00
        profit: float = (float(this[-1][1]) * float(this[-1][2]) / 100)

        if len(this[-1]) < 4:
            this[-1].append(f"{profit:.2f}")

        if len(this) > 0:
            for ts in this:
                spend += int(ts[1])
                profit_all += (float(ts[1]) * float(ts[2]) / 100)

        this.insert(0, [spend, f"{profit_all:.2f}"])
        possibility.append(this)

best = sorted(possibility, key=lambda x: x[0][1], reverse=True)

for bt in best:
    rotate += 1
    if 500 > int(bt[0][0]) > 480:
        possibilities.append(bt)

stop = time.time()
space_time: float = "{:.4f}".format((stop - start))

if __name__ == "__main__":

    the_best = possibilities[0]

    print(f"== {"{:,}".format(rotate).replace(",", " ")} résultats \n \n"
          f"MEILLEUR RESULTAT : \n"
          f"== {len(the_best) - 1} Actions \n"
          f"== Cout : {"{:.2f}".format(float(the_best[0][0]))} € \n"
          f"== Profit : {"{:.2f}".format(float(the_best[0][1]))} € \n"
          f"== Temps d'exécution : {space_time} \n")

    the_best.remove(the_best[0])
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Nom", style="dim", width=12)
    table.add_column("Coût", justify="right")
    table.add_column("Pourcentage", justify="right")
    table.add_column("Gains", justify="right")

    for act in the_best:
        cout = f"{float(act[1]):.2f} €"
        pourcent = f"{float(act[2]):.2f} %"
        table.add_row(act[0], cout, pourcent, f"{act[3]} €")

    console.print(table, style="bold green on blue")
