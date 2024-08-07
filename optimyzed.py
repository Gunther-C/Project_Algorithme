from rich.console import Console
from rich.table import Table
import csv
import time


class Optimized:
    def __init__(self, path: str | None = None) -> None:

        new_file: list = []
        try:
            with open(path, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader)
                [new_file.append(i) for i in reader]
        except IOError as er:
            print("Erreur lors de l'ouverture du fichier :", er)
        except UnicodeEncodeError as err:
            print("Erreur D'encodage :", err)

        if len(new_file) > 0:
            self.treatment(new_file)

    @staticmethod
    def treatment(datas: list) -> list:
        """
        _ Suppression des actions coût inférieur ou égal à zéro
        _ Classification des actions par leur pourçentage de bénéfice + > -
        _ Création de la best liste coût maxi 500
        :param datas: datas
        :return: Best liste
        BigO : O(1)
        """

        start = time.time()
        rotate = 0

        new_list = []
        [new_list.append(fls) for fls in datas if float(fls[1]) > 0]

        best = sorted(new_list, key=lambda x: float(x[2]), reverse=True)

        best_list = []
        spend: float = 0.00
        profit_all: float = 0.00

        for this in best:
            rotate += 1
            profit = float("{:.2f}".format((float(this[1]) * float(this[2]) / 100)))
            new_spend = float("{:.2f}".format(spend + float(this[1])))

            if 500 > new_spend and profit > 0:
                spend = new_spend
                profit_all += profit
                this.append(f"{profit:.2f}")
                best_list.append(this)

        stop = time.time()
        space_time: float = "{:.4f}".format((stop - start))

        print(f"== {"{:,}".format(rotate).replace(",", " ")} résultats \n \n"
              f"MEILLEUR RESULTAT : \n"
              f"== {len(best_list)} Actions \n"
              f"== Cout : {spend:.2f} € \n"
              f"== Profit : {profit_all:.2f} € \n"
              f"== Temps d'exécution : {space_time} \n")

        console = Console()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Nom", style="dim", width=12)
        table.add_column("Coût", justify="right")
        table.add_column("Pourcentage", justify="right")
        table.add_column("Gains", justify="right")

        for act in best_list:
            cout = f"{float(act[1]):.2f} €"
            pourcent = f"{float(act[2]):.2f} %"
            table.add_row(act[0], cout, pourcent, f"{act[3]} €")

        console.print(table, style="bold green on blue")


if __name__ == "__main__":
    force_brute = "data_csv/force_brute.csv"
    data_sets1 = "data_csv/dataset1.csv"
    data_sets2 = "data_csv/dataset2.csv"
    Optimized(data_sets1)
