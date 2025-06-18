import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)

        # KPI-блоки
        kpi_frame = tk.Frame(self)
        kpi_frame.pack(fill="x", pady=10)
        self.kpi_labels = []
        kpi_titles = [
            "Общий объём продаж (₽)",
            "Средний чек (₽)",
            "Количество заказов",
            "Выполнение плана (%)",
        ]
        kpi_values = [ "120 000", "850", "142", "97%" ] # временные значения
        for i, (title, value) in enumerate(zip(kpi_titles, kpi_values)):
            block = tk.LabelFrame(kpi_frame, text=title, padx=10, pady=10)
            block.pack(side="left", expand=True, fill="x", padx=5)
            lbl = tk.Label(block, text=value, font=("Arial", 18, "bold"))
            lbl.pack()
            self.kpi_labels.append(lbl)

        # Фильтры
        filter_frame = tk.LabelFrame(self, text="Фильтры")
        filter_frame.pack(fill="x", pady=10, padx=5)
        tk.Label(filter_frame, text="Время:").pack(side="left", padx=5)
        self.time_var = tk.StringVar(value="День")
        ttk.Combobox(filter_frame, textvariable=self.time_var, values=["День", "Неделя", "Месяц"], width=8).pack(side="left")

        tk.Label(filter_frame, text="Продукт:").pack(side="left", padx=5)
        self.product_var = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.product_var, values=["Все", "Пиццы", "Напитки", "Десерты"], width=10).pack(side="left")

        tk.Label(filter_frame, text="Филиал:").pack(side="left", padx=5)
        self.branch_var = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.branch_var, values=["Все", "Центр", "Север", "Юг"], width=10).pack(side="left")

        # Графики
        charts_frame = tk.Frame(self)
        charts_frame.pack(fill="both", expand=True, padx=5, pady=10)
        chart1 = tk.LabelFrame(charts_frame, text="Динамика продаж (линейный график)")
        chart1.pack(side="left", expand=True, fill="both", padx=5)
        tk.Label(chart1, text="График здесь", fg="gray").pack(expand=True)
        chart2 = tk.LabelFrame(charts_frame, text="Распределение по категориям (круговая диаграмма)")
        chart2.pack(side="left", expand=True, fill="both", padx=5)
        tk.Label(chart2, text="Диаграмма здесь", fg="gray").pack(expand=True)

        # Панель уведомлений
        notif_frame = tk.LabelFrame(self, text="Уведомления")
        notif_frame.pack(fill="x", padx=5, pady=5)
        notifications = [
            "Низкий уровень сыра — закажите поставку",
            "Заканчивается упаковка для пиццы",
        ]
        for note in notifications:
            tk.Label(notif_frame, text=note, fg="red").pack(anchor="w")

# Остальной код структуры приложения из предыдущего этапа:
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("АРМ Руководителя отдела продаж пиццерии")
        self.geometry("1100x700")

        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top", fill="x")
        self.pages = {}
        buttons = [
            ("Дашборд", DashboardPage),
            ("Аналитика", AnalyticsPage),
            ("Запасы", StockPage),
            ("Персонал", StaffPage),
            ("Финансы", FinancePage),
        ]
        for (text, PageClass) in buttons:
            btn = tk.Button(nav_frame, text=text, command=lambda p=PageClass: self.show_page(p))
            btn.pack(side="left", padx=5, pady=5)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        for _, PageClass in buttons:
            page = PageClass(self.container, self)
            self.pages[PageClass] = page
            page.grid(row=0, column=0, sticky="nsew")
        self.show_page(DashboardPage)

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

class AnalyticsPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        # Фильтры
        filter_frame = tk.LabelFrame(self, text="Фильтры")
        filter_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(filter_frame, text="Время:").pack(side="left", padx=5)
        self.time_var = tk.StringVar(value="Месяц")
        ttk.Combobox(filter_frame, textvariable=self.time_var, values=["День", "Неделя", "Месяц"], width=8).pack(side="left")
        tk.Label(filter_frame, text="Регион:").pack(side="left", padx=5)
        self.region_var = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.region_var, values=["Все", "Центр", "Север", "Юг"], width=10).pack(side="left")

        # Таблица заказов
        orders_frame = tk.LabelFrame(self, text="Сводка по заказам")
        orders_frame.pack(fill="x", padx=5, pady=5)
        self.orders_table = ttk.Treeview(orders_frame, columns=("num", "date", "sum", "status"), show='headings', height=5)
        self.orders_table.heading("num", text="№ заказа")
        self.orders_table.heading("date", text="Дата")
        self.orders_table.heading("sum", text="Сумма (₽)")
        self.orders_table.heading("status", text="Статус")
        self.orders_table.pack(fill="x")
        # Пример данных
        for row in [
            (101, "2025-06-10", "1250", "Выполнен"),
            (102, "2025-06-10", "980", "Выполнен"),
            (103, "2025-06-11", "2100", "Выполнен"),
            (104, "2025-06-11", "560", "Отменён"),
        ]:
            self.orders_table.insert("", "end", values=row)

        # Таблица по продуктам
        products_frame = tk.LabelFrame(self, text="Данные по продуктам")
        products_frame.pack(fill="x", padx=5, pady=5)
        self.products_table = ttk.Treeview(products_frame, columns=("name", "qty", "profit"), show='headings', height=5)
        self.products_table.heading("name", text="Название")
        self.products_table.heading("qty", text="Кол-во заказов")
        self.products_table.heading("profit", text="Прибыль (₽)")
        self.products_table.pack(fill="x")
        # Пример данных
        for row in [
            ("Пицца Маргарита", 34, 17000),
            ("Пицца Пепперони", 41, 25000),
            ("Лимонад", 60, 9000),
            ("Тирамису", 15, 4500),
        ]:
            self.products_table.insert("", "end", values=row)

        # Графики (заглушки)
        charts_frame = tk.Frame(self)
        charts_frame.pack(fill="both", expand=True, padx=5, pady=5)
        chart1 = tk.LabelFrame(charts_frame, text="Гистограмма по категориям товаров")
        chart1.pack(side="left", expand=True, fill="both", padx=5)
        tk.Label(chart1, text="График здесь", fg="gray").pack(expand=True)
        chart2 = tk.LabelFrame(charts_frame, text="Динамика по филиалам (линейный график)")
        chart2.pack(side="left", expand=True, fill="both", padx=5)
        tk.Label(chart2, text="График здесь", fg="gray").pack(expand=True)

        # Таблица с деталями по регионам и каналам продаж
        details_frame = tk.LabelFrame(self, text="Аналитика по регионам и каналам продаж")
        details_frame.pack(fill="x", padx=5, pady=5)
        self.details_table = ttk.Treeview(details_frame, columns=("region", "channel", "orders", "profit"), show='headings', height=3)
        self.details_table.heading("region", text="Регион")
        self.details_table.heading("channel", text="Канал")
        self.details_table.heading("orders", text="Кол-во заказов")
        self.details_table.heading("profit", text="Прибыль (₽)")
        self.details_table.pack(fill="x")
        for row in [
            ("Центр", "Зал", 32, 15000),
            ("Север", "Доставка", 28, 13000),
            ("Юг", "Самовывоз", 15, 5000),
        ]:
            self.details_table.insert("", "end", values=row)

        # Кнопки для функций
        actions_frame = tk.Frame(self)
        actions_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(actions_frame, text="Экспорт отчёта", command=self.export_report).pack(side="left", padx=5)
        tk.Button(actions_frame, text="Анализ популярных товаров", command=self.analyze_popular).pack(side="left", padx=5)

    def export_report(self):
        tk.messagebox.showinfo("Экспорт", "Экспорт отчёта пока не реализован.")

    def analyze_popular(self):
        tk.messagebox.showinfo("Анализ", "Функция анализа популярных товаров пока не реализована.")

# Остальная структура приложения (MainApp и другие страницы) остаётся как на предыдущем этапе.

class StockPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        # Фильтры (по желанию)
        filter_frame = tk.LabelFrame(self, text="Фильтры")
        filter_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(filter_frame, text="Категория:").pack(side="left", padx=5)
        self.category_var = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.category_var, values=["Все", "Овощи", "Молочные", "Мясо", "Тесто", "Другое"], width=12).pack(side="left")

        # Таблица ингредиентов
        ingredients_frame = tk.LabelFrame(self, text="Ингредиенты")
        ingredients_frame.pack(fill="x", padx=5, pady=5)
        self.ingredients_table = ttk.Treeview(
            ingredients_frame,
            columns=("name", "current", "min", "status"),
            show='headings',
            height=7
        )
        self.ingredients_table.heading("name", text="Название")
        self.ingredients_table.heading("current", text="Текущий остаток")
        self.ingredients_table.heading("min", text="Мин. уровень")
        self.ingredients_table.heading("status", text="Статус")
        self.ingredients_table.pack(fill="x")

        # Пример данных
        for row in [
            ("Моцарелла", 3.2, 2.0, "OK"),
            ("Тесто", 1.0, 1.5, "Нужно заказать"),
            ("Ветчина", 2.5, 1.0, "OK"),
            ("Помидоры", 0.8, 1.0, "Низкий уровень"),
            ("Пармезан", 0.5, 0.7, "Нужно заказать"),
        ]:
            self.ingredients_table.insert("", "end", values=row)

        # График использования (пока заглушка)
        usage_frame = tk.LabelFrame(self, text="Динамика использования ингредиентов")
        usage_frame.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Label(usage_frame, text="График здесь", fg="gray").pack(expand=True)

        # Панель уведомлений
        notif_frame = tk.LabelFrame(self, text="Уведомления")
        notif_frame.pack(fill="x", padx=5, pady=5)
        notifications = [
            "Заканчивается тесто — необходим заказ!",
            "Низкий уровень помидоров!",
            "Пармезан на минимуме.",
        ]
        for note in notifications:
            tk.Label(notif_frame, text=note, fg="red").pack(anchor="w")

class StaffPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        
        # Таблица сотрудников
        staff_frame = tk.LabelFrame(self, text="Сотрудники")
        staff_frame.pack(fill="x", padx=5, pady=5)
        self.staff_table = ttk.Treeview(
            staff_frame,
            columns=("name", "role", "orders", "efficiency"),
            show='headings',
            height=6
        )
        self.staff_table.heading("name", text="Имя")
        self.staff_table.heading("role", text="Должность")
        self.staff_table.heading("orders", text="Кол-во заказов")
        self.staff_table.heading("efficiency", text="Производительность (%)")
        self.staff_table.pack(fill="x")
        # Пример данных
        for row in [
            ("Иванов И.И.", "Оператор", 32, 88),
            ("Петрова А.А.", "Кассир", 40, 92),
            ("Сидоров В.В.", "Пиццмейкер", 28, 83),
            ("Лебедева О.О.", "Курьер", 45, 97),
        ]:
            self.staff_table.insert("", "end", values=row)

        # График эффективности (заглушка)
        chart_frame = tk.LabelFrame(self, text="График эффективности сотрудников")
        chart_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(chart_frame, text="График здесь", fg="gray").pack(expand=True)

        # Время работы в сменах
        shifts_frame = tk.LabelFrame(self, text="Работа в сменах")
        shifts_frame.pack(fill="x", padx=5, pady=5)
        self.shifts_table = ttk.Treeview(
            shifts_frame,
            columns=("name", "shift", "hours"),
            show='headings',
            height=4
        )
        self.shifts_table.heading("name", text="Имя")
        self.shifts_table.heading("shift", text="Смена")
        self.shifts_table.heading("hours", text="Часы за период")
        self.shifts_table.pack(fill="x")
        for row in [
            ("Иванов И.И.", "Утренняя", 36),
            ("Петрова А.А.", "Вечерняя", 40),
            ("Сидоров В.В.", "Дневная", 32),
        ]:
            self.shifts_table.insert("", "end", values=row)

        # Панель управления сменами
        control_frame = tk.LabelFrame(self, text="Панель управления сменами")
        control_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(control_frame, text="Назначить смену", command=self.assign_shift).pack(side="left", padx=5)
        tk.Button(control_frame, text="Изменить смену", command=self.change_shift).pack(side="left", padx=5)
        tk.Button(control_frame, text="Удалить смену", command=self.delete_shift).pack(side="left", padx=5)

        # Уведомления о сменах
        notif_frame = tk.LabelFrame(self, text="Уведомления")
        notif_frame.pack(fill="x", padx=5, pady=5)
        notifications = [
            "Назначена новая смена для Иванова И.И.",
            "Петрова А.А. сегодня в вечерней смене.",
        ]
        for note in notifications:
            tk.Label(notif_frame, text=note, fg="blue").pack(anchor="w")

    def assign_shift(self):
        tk.messagebox.showinfo("Назначить смену", "Функция назначения смены пока не реализована.")

    def change_shift(self):
        tk.messagebox.showinfo("Изменить смену", "Функция изменения смены пока не реализована.")

    def delete_shift(self):
        tk.messagebox.showinfo("Удалить смену", "Функция удаления смены пока не реализована.")

class FinancePage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)

        # Таблица доходов и расходов
        report_frame = tk.LabelFrame(self, text="Отчёты о доходах и расходах")
        report_frame.pack(fill="x", padx=5, pady=5)
        self.report_table = ttk.Treeview(
            report_frame,
            columns=("date", "income", "expense", "profit"),
            show='headings',
            height=7
        )
        self.report_table.heading("date", text="Период")
        self.report_table.heading("income", text="Доходы (₽)")
        self.report_table.heading("expense", text="Расходы (₽)")
        self.report_table.heading("profit", text="Прибыль (₽)")
        self.report_table.pack(fill="x")

        # Пример данных
        for row in [
            ("2025-06-01", 120000, 80000, 40000),
            ("2025-06-02", 130000, 85000, 45000),
            ("2025-06-03", 110000, 78000, 32000),
            ("2025-06-04", 140000, 90000, 50000),
            ("2025-06-05", 135000, 88000, 47000),
        ]:
            self.report_table.insert("", "end", values=row)

        # График прибыли (заглушка)
        chart_frame = tk.LabelFrame(self, text="График прибыли")
        chart_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(chart_frame, text="График здесь", fg="gray").pack(expand=True)

        # Панель прогноза
        forecast_frame = tk.LabelFrame(self, text="Панель прогноза")
        forecast_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(forecast_frame, text="Прогноз прибыли на следующую неделю: 320 000 ₽", font=("Arial", 12, "bold"), fg="green").pack(anchor="w")
        tk.Label(forecast_frame, text="Ожидаемый рост: +5% по сравнению с прошлой неделей", fg="blue").pack(anchor="w")
        tk.Label(forecast_frame, text="Рекомендация: усилить продажи по акции 'Лето с пиццей!'", fg="black").pack(anchor="w")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

