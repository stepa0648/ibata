import matplotlib.pyplot as plt


class PlotMaker:
    """Class for making plot from result"""

    @staticmethod
    def show_and_save_plot(categories_summary, should_show_plot):
        """Shows and saves plot to {date_from}_{date_to}.png"""
        if should_show_plot:
            plt.figure(figsize=(10, 10))
            categories_names = []
            categories_amounts = []
            for category in categories_summary.categories:
                if category.amount == 0:
                    continue
                categories_names.append(category.name_pretty)
                categories_amounts.append(abs(category.amount))
            plt.bar(categories_names, categories_amounts)
            plt.xlabel('Kategorie')
            plt.ylabel('Absolutní hodnota v Kč')
            plt.title(f"Výdaje a příjmy {categories_summary.date_from} - {categories_summary.date_to}")
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.savefig(f'{categories_summary.date_from}_{categories_summary.date_to}.png')
            plt.show()
