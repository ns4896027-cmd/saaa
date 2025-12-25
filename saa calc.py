import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


class AgriculturePriceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор цен продукции растениеводства")
        self.root.geometry("600x700")

        # Инициализация переменных
        self.markup_percentages = {
            'Ячмень': 50,
            'Озимая пшеница': 35,
            'Подсолнечник': 45
        }
        self.insurance_rate = 0.30

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Расчет реализационной цены сельхозпродукции")
        title_label.pack(anchor='w', padx=20, pady=10)

        # Тип культуры
        tk.Label(self.root, text="Тип культуры:").pack(anchor='w', padx=20)

        self.culture_var = tk.StringVar(value='Ячмень')
        self.culture_combo = ttk.Combobox(
            self.root,
            textvariable=self.culture_var,
            values=['Ячмень', 'Озимая пшеница', 'Подсолнечник'],
            state='readonly',
            width=30
        )
        self.culture_combo.pack(anchor='w', padx=20, pady=5)

        # Поля ввода (все слева)
        self.create_left_input("Производственная себестоимость 1 ц, тыс. руб.:", "cost")
        self.create_left_input("Объем реализации, ц:", "volume")
        self.create_left_input("Аренда торговой точки, тыс. руб.:", "rent")
        self.create_left_input("Заработная плата продавцам, тыс. руб.:", "salary")
        self.create_left_input("Маркетинговые расходы, тыс. руб.:", "marketing")

        # Страховые взносы
        tk.Label(self.root, text="Страховые взносы, тыс. руб.:").pack(anchor='w', padx=20)

        self.insurance_button = tk.Button(
            self.root,
            text="Рассчитать страховые взносы",
            command=self.calculate_insurance
        )
        self.insurance_button.pack(anchor='w', padx=20, pady=5)

        self.insurance_result = tk.Entry(self.root, width=30, state='readonly')
        self.insurance_result.pack(anchor='w', padx=20, pady=5)

        # Уровень наценки
        tk.Label(self.root, text="Уровень наценки, %:").pack(anchor='w', padx=20)

        self.markup_button = tk.Button(
            self.root,
            text="Определить наценку",
            command=self.show_markup
        )
        self.markup_button.pack(anchor='w', padx=20, pady=5)

        self.markup_result = tk.Entry(self.root, width=30, state='readonly')
        self.markup_result.pack(anchor='w', padx=20, pady=5)

        # Цена реализации
        tk.Label(self.root, text="Цена реализации, тыс. руб.:").pack(anchor='w', padx=20)

        self.price_button = tk.Button(
            self.root,
            text="Рассчитать цену реализации",
            command=self.calculate_price
        )
        self.price_button.pack(anchor='w', padx=20, pady=5)

        self.price_result = tk.Entry(self.root, width=30, state='readonly')
        self.price_result.pack(anchor='w', padx=20, pady=5)

        # Плановая цена
        tk.Label(self.root, text="Плановая цена для сравнения, тыс. руб.:").pack(anchor='w', padx=20)
        self.planned_input = tk.Entry(self.root, width=30)
        self.planned_input.pack(anchor='w', padx=20, pady=5)

        # Кнопки (тоже слева)
        self.compare_button = tk.Button(
            self.root,
            text="Сравнение цен (построить гистограмму)",
            command=self.show_comparison_chart
        )
        self.compare_button.pack(anchor='w', padx=20, pady=10)


    def create_left_input(self, label_text, field_name):
        tk.Label(self.root, text=label_text).pack(anchor='w', padx=20)
        entry = tk.Entry(self.root, width=30)
        entry.pack(anchor='w', padx=20, pady=5)
        setattr(self, f"{field_name}_input", entry)

    def calculate_insurance(self):

            salary_text = self.salary_input.get()
            if salary_text:
                salary = float(salary_text)
                insurance = salary * self.insurance_rate
                self.insurance_result.config(state='normal')
                self.insurance_result.delete(0, tk.END)
                self.insurance_result.insert(0, f"{insurance:.2f}")
                self.insurance_result.config(state='readonly')


    def show_markup(self):
        culture = self.culture_var.get()
        markup = self.markup_percentages.get(culture, 0)

        self.markup_result.config(state='normal')
        self.markup_result.delete(0, tk.END)
        self.markup_result.insert(0, f"{markup}%")
        self.markup_result.config(state='readonly')

        messagebox.showinfo("Уровень наценки", f"Для культуры '{culture}' установлена наценка: {markup}%")

    def calculate_price(self):
            # Получаем значения
            cost = float(self.cost_input.get()) if self.cost_input.get() else 0
            rent = float(self.rent_input.get()) if self.rent_input.get() else 0
            salary = float(self.salary_input.get()) if self.salary_input.get() else 0
            marketing = float(self.marketing_input.get()) if self.marketing_input.get() else 0

            # Страховые взносы
            insurance_text = self.insurance_result.get()
            insurance = float(insurance_text) if insurance_text else salary * self.insurance_rate

            # Наценка
            culture = self.culture_var.get()
            markup = self.markup_percentages.get(culture, 0)

            # Расчет
            total_additional_costs = rent + salary + insurance + marketing
            price_per_unit = (cost + total_additional_costs) * (1 + markup / 100)

            # Вывод результата
            self.price_result.config(state='normal')
            self.price_result.delete(0, tk.END)
            self.price_result.insert(0, f"{price_per_unit:.2f}")
            self.price_result.config(state='readonly')


    def show_comparison_chart(self):

            actual_price_text = self.price_result.get()
            planned_price_text = self.planned_input.get()

            actual_price = float(actual_price_text)
            planned_price = float(planned_price_text)
            culture = self.culture_var.get()

            # Создаем гистограмму
            fig, ax = plt.subplots(figsize=(8, 5))

            labels = ['Фактическая цена', 'Плановая цена']
            prices = [actual_price, planned_price]
            colors = ['blue', 'orange']

            bars = ax.bar(labels, prices, color=colors)

            # Добавляем значения
            for bar, price in zip(bars, prices):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{price:.2f}',
                        ha='center', va='bottom')

            ax.set_title(f'Сравнение цен для культуры: {culture}')
            ax.set_ylabel('Цена, тыс. руб.')
            ax.set_xlabel('Тип цены')
            plt.show()
if __name__ == "__main__":
    root = tk.Tk()
    app = AgriculturePriceCalculator(root)
    root.mainloop()