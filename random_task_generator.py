import json
import random
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox


HISTORY_FILE = Path("task_history.json")
TASKS_FILE = Path("tasks.json")

DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "Учёба"},
    {"text": "Повторить тему по программированию", "type": "Учёба"},
    {"text": "Решить 5 задач", "type": "Учёба"},
    {"text": "Сделать зарядку", "type": "Спорт"},
    {"text": "Пройти 3000 шагов", "type": "Спорт"},
    {"text": "Сделать растяжку", "type": "Спорт"},
    {"text": "Разобрать рабочие заметки", "type": "Работа"},
    {"text": "Составить план на день", "type": "Работа"},
    {"text": "Ответить на важные сообщения", "type": "Работа"},
]

TASK_TYPES = ["Все", "Учёба", "Спорт", "Работа"]


class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("780x560")
        self.root.minsize(720, 500)

        self.tasks = self.load_tasks()
        self.history = self.load_history()

        self.selected_filter = tk.StringVar(value="Все")
        self.new_task_text = tk.StringVar()
        self.new_task_type = tk.StringVar(value="Учёба")
        self.current_task = tk.StringVar(value="Нажмите кнопку, чтобы сгенерировать задачу")

        self.create_widgets()
        self.refresh_history_list()

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Random Task Generator",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=12)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        generator_frame = ttk.LabelFrame(main_frame, text="Генерация задачи", padding=10)
        generator_frame.pack(fill="x", pady=5)

        ttk.Label(generator_frame, text="Фильтр по типу задачи:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        filter_box = ttk.Combobox(
            generator_frame,
            textvariable=self.selected_filter,
            values=TASK_TYPES,
            state="readonly",
            width=18
        )
        filter_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        generate_button = ttk.Button(
            generator_frame,
            text="Сгенерировать задачу",
            command=self.generate_task
        )
        generate_button.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        current_label = ttk.Label(
            generator_frame,
            textvariable=self.current_task,
            font=("Arial", 13),
            wraplength=680
        )
        current_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=12)

        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", pady=8)

        ttk.Label(add_frame, text="Текст задачи:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        entry = ttk.Entry(add_frame, textvariable=self.new_task_text, width=45)
        entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_frame, text="Тип:").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        type_box = ttk.Combobox(
            add_frame,
            textvariable=self.new_task_type,
            values=TASK_TYPES[1:],
            state="readonly",
            width=14
        )
        type_box.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        add_button = ttk.Button(add_frame, text="Добавить", command=self.add_task)
        add_button.grid(row=0, column=4, sticky="w", padx=5, pady=5)

        add_frame.columnconfigure(1, weight=1)

        history_frame = ttk.LabelFrame(main_frame, text="История сгенерированных задач", padding=10)
        history_frame.pack(fill="both", expand=True, pady=8)

        self.history_listbox = tk.Listbox(history_frame, height=12)
        self.history_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=5)

        clear_button = ttk.Button(bottom_frame, text="Очистить историю", command=self.clear_history)
        clear_button.pack(side="right")

    def load_tasks(self):
        if TASKS_FILE.exists():
            try:
                with TASKS_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, list) and data:
                    valid_tasks = []
                    for item in data:
                        if (
                            isinstance(item, dict)
                            and isinstance(item.get("text"), str)
                            and item.get("text").strip()
                            and item.get("type") in TASK_TYPES[1:]
                        ):
                            valid_tasks.append({
                                "text": item["text"].strip(),
                                "type": item["type"]
                            })
                    if valid_tasks:
                        return valid_tasks
            except json.JSONDecodeError:
                messagebox.showwarning(
                    "Ошибка загрузки",
                    "Файл tasks.json повреждён. Будут использованы стандартные задачи."
                )
        return DEFAULT_TASKS.copy()

    def save_tasks(self):
        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    def load_history(self):
        if HISTORY_FILE.exists():
            try:
                with HISTORY_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                messagebox.showwarning(
                    "Ошибка загрузки",
                    "Файл task_history.json повреждён. История будет очищена."
                )
        return []

    def save_history(self):
        with HISTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)

    def get_available_tasks(self):
        selected_type = self.selected_filter.get()
        if selected_type == "Все":
            return self.tasks
        return [task for task in self.tasks if task["type"] == selected_type]

    def generate_task(self):
        available_tasks = self.get_available_tasks()

        if not available_tasks:
            messagebox.showerror(
                "Нет задач",
                "Для выбранного типа задач список пуст. Добавьте новую задачу."
            )
            return

        task = random.choice(available_tasks)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        history_item = {
            "time": timestamp,
            "task": task["text"],
            "type": task["type"]
        }

        self.history.append(history_item)
        self.save_history()

        self.current_task.set(f"{task['type']}: {task['text']}")
        self.refresh_history_list()

    def add_task(self):
        text = self.new_task_text.get().strip()
        task_type = self.new_task_type.get()

        if not text:
            messagebox.showerror("Ошибка ввода", "Задача не может быть пустой строкой.")
            return

        if task_type not in TASK_TYPES[1:]:
            messagebox.showerror("Ошибка ввода", "Выберите корректный тип задачи.")
            return

        self.tasks.append({"text": text, "type": task_type})
        self.save_tasks()

        self.new_task_text.set("")
        messagebox.showinfo("Успешно", "Новая задача добавлена.")

    def refresh_history_list(self):
        self.history_listbox.delete(0, tk.END)

        if not self.history:
            self.history_listbox.insert(tk.END, "История пока пуста.")
            return

        for item in reversed(self.history):
            line = f"{item.get('time', 'без даты')} | {item.get('type', 'тип не указан')} | {item.get('task', '')}"
            self.history_listbox.insert(tk.END, line)

    def clear_history(self):
        if not self.history:
            return

        answer = messagebox.askyesno("Подтверждение", "Очистить всю историю?")
        if answer:
            self.history.clear()
            self.save_history()
            self.refresh_history_list()
            self.current_task.set("История очищена.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()
