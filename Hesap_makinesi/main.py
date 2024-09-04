import tkinter as tk
from tkinter import ttk, colorchooser
from sympy import sympify
import binascii
import json

class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hesap Makinesi")
        self.geometry("600x700")

        self.settings = self.load_settings()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.create_calculator_tab()
        self.create_conversion_tab()
        self.create_settings_tab()

        self.apply_settings()

    def create_calculator_tab(self):
        self.calculator_frame = tk.Frame(self.notebook, bg=self.settings["background_color"])
        self.notebook.add(self.calculator_frame, text='Hesap Makinesi')

        self.result_frame = tk.Frame(self.calculator_frame, bg=self.settings["button_color"])
        self.result_frame.pack(expand=True, fill='both')

        self.expression_var = tk.StringVar()
        self.expression_entry = tk.Entry(
            self.result_frame, textvariable=self.expression_var, font=('Arial', 18), bd=10, relief='ridge',
            justify='left', bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.expression_entry.pack(expand=True, fill='both')

        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(
            self.result_frame, textvariable=self.result_var, font=('Arial', 18), bd=10, relief='ridge',
            justify='right', bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.result_entry.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self.calculator_frame, bg=self.settings["background_color"])
        self.button_frame.pack(expand=True, fill='both')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('%', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('1/x', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('√', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('^', 4, 3), ('(', 4, 4),
            (')', 5, 0), ('C', 5, 1), ('<', 5, 2), ('tan', 5, 3), ('cos', 5, 4),
            ('sin', 6, 0), ('log', 6, 1), ('π', 6, 2), ('e', 6, 3), ('=', 6, 4),
        ]

        self.buttons = {}
        for (text, row, col) in buttons:
            button = tk.Button(
                self.button_frame, text=text, font=('Arial', 18), bd=1, relief='flat',
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, padx=0, pady=0, sticky='nsew')
            self.buttons[text] = button

        for i in range(7):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.button_frame.grid_columnconfigure(j, weight=1)

    def create_conversion_tab(self):
        conversion_frame = tk.Frame(self.notebook, bg=self.settings["background_color"])
        self.notebook.add(conversion_frame, text='Dönüştürme')

        tk.Label(
            conversion_frame, text='Girdi:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=5)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            conversion_frame, textvariable=self.input_var, font=('Arial', 14), bd=10, relief='ridge',
            bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.input_entry.pack(expand=True, fill='x', padx=10, pady=5)

        tk.Label(
            conversion_frame, text='Çıktı:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=5)
        self.output_var = tk.StringVar()
        self.output_entry = tk.Entry(
            conversion_frame, textvariable=self.output_var, font=('Arial', 14), bd=10, relief='ridge',
            bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.output_entry.pack(expand=True, fill='x', padx=10, pady=5)

        self.input_type = tk.StringVar(value='decimal')
        self.output_type = tk.StringVar(value='decimal')

        types = ['hexadecimal', 'binary', 'decimal',]
        tk.Label(
            conversion_frame, text='Girdi Türü:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=5)
        self.input_type_menu = tk.OptionMenu(conversion_frame, self.input_type, *types)
        self.input_type_menu.pack(pady=5)

        tk.Label(
            conversion_frame, text='Çıktı Türü:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=5)
        self.output_type_menu = tk.OptionMenu(conversion_frame, self.output_type, *types)
        self.output_type_menu.pack(pady=5)

        self.input_entry.bind('<KeyRelease>', self.convert)

    def create_settings_tab(self):
        settings_frame = tk.Frame(self.notebook, bg=self.settings["background_color"])
        self.notebook.add(settings_frame, text='Ayarlar')

        tk.Label(
            settings_frame, text='Arka Plan Rengi:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=10)
        self.bg_color_btn = tk.Button(
            settings_frame, text="Renk Seç", command=self.change_bg_color, bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.bg_color_btn.pack(pady=10)

        tk.Label(
            settings_frame, text='Yazı Rengi:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=10)
        self.text_color_btn = tk.Button(
            settings_frame, text="Renk Seç", command=self.change_text_color, bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.text_color_btn.pack(pady=10)

        tk.Label(
            settings_frame, text='Buton Rengi:', font=('Arial', 14), bg=self.settings["background_color"], fg=self.settings["text_color"]
        ).pack(pady=10)
        self.button_color_btn = tk.Button(
            settings_frame, text="Renk Seç", command=self.change_button_color, bg=self.settings["button_color"], fg=self.settings["text_color"]
        )
        self.button_color_btn.pack(pady=10)

        tk.Button(
            settings_frame, text="Kaydet", command=self.save_settings, bg=self.settings["button_color"], fg=self.settings["text_color"]
        ).pack(pady=20)

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Arka Plan Rengi Seç")[1]
        if color:
            self.settings["background_color"] = color
            self.apply_settings()

    def change_text_color(self):
        color = colorchooser.askcolor(title="Yazı Rengi Seç")[1]
        if color:
            self.settings["text_color"] = color
            self.apply_settings()

    def change_button_color(self):
        color = colorchooser.askcolor(title="Buton Rengi Seç")[1]
        if color:
            self.settings["button_color"] = color
            self.apply_settings()

    def apply_settings(self):
        for tab in self.notebook.tabs():
            frame = self.notebook.nametowidget(tab)
            frame.config(bg=self.settings["background_color"])
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg=self.settings["background_color"])
                elif isinstance(widget, tk.Label):
                    widget.config(bg=self.settings["background_color"], fg=self.settings["text_color"])
                elif isinstance(widget, tk.Button):
                    widget.config(bg=self.settings["button_color"], fg=self.settings["text_color"])
                elif isinstance(widget, tk.Entry):
                    widget.config(bg=self.settings["button_color"], fg=self.settings["text_color"])
                elif isinstance(widget, tk.OptionMenu):
                    menu = widget.children['menu']
                    menu.config(bg=self.settings["button_color"], fg=self.settings["text_color"])
                    widget.config(bg=self.settings["button_color"], fg=self.settings["text_color"])

        for button in self.button_frame.winfo_children():
            button.config(bg=self.settings["button_color"], fg=self.settings["text_color"])

        self.result_entry.config(bg=self.settings["button_color"], fg=self.settings["text_color"])
        self.input_entry.config(bg=self.settings["button_color"], fg=self.settings["text_color"])
        self.expression_entry.config(bg=self.settings["button_color"], fg=self.settings["text_color"])

        self.button_frame.config(bg=self.settings["background_color"])

    def save_settings(self):
        with open('ayarlar.json', 'w') as f:
            json.dump(self.settings, f)

    def load_settings(self):
        try:
            with open('ayarlar.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "background_color": "#FFFFFF",
                "text_color": "#000000",
                "button_color": "#F0F0F0"
            }

    def on_button_click(self, text):
        current_text = self.expression_var.get()

        if text == 'C':
            self.expression_var.set("")
            self.result_var.set("")
        elif text == '=':
            try:
                expression = current_text.replace('^', '**')
                expression = expression.replace('tan', 'tan')
                expression = expression.replace('cos', 'cos')
                expression = expression.replace('sin', 'sin')
                expression = expression.replace('log', 'log')
                expression = expression.replace('π', 'pi')
                expression = expression.replace('e', 'E')
                expression = expression.replace('√', 'sqrt')
                result = sympify(expression).evalf()
                result = abs(result)
                self.result_var.set(f"{result:.2f}")
            except Exception:
                self.result_var.set("Hata")
        elif text == '<':
            self.expression_var.set(current_text[:-1])
        elif text == '1/x':
            try:
                result = 1 / float(current_text)
                self.result_var.set(f"{result:.2f}")
            except Exception:
                self.result_var.set("Hata")
        elif text == 'π':
            self.expression_var.set(current_text + 'π')
        elif text == 'e':
            self.expression_var.set(current_text + 'e')
        elif text == '√':
            if current_text and current_text[-1].isdigit():
                self.expression_var.set(current_text + '√(')
            else:
                self.expression_var.set(current_text + 'sqrt(')
        elif text == '^':
            self.expression_var.set(current_text + '^')
        else:
            self.expression_var.set(current_text + text)


    def convert(self, event=None):
        input_value = self.input_var.get()
        input_type = self.input_type.get()
        output_type = self.output_type.get()

        try:
            if input_type == 'hexadecimal':
                decimal_value = int(input_value, 16)
            elif input_type == 'binary':
                decimal_value = int(input_value, 2)
            elif input_type == 'decimal':
                decimal_value = int(input_value)
            else:
                self.output_var.set("Hata")
                return

            if output_type == 'hexadecimal':
                output_value = hex(decimal_value)[2:].upper()
            elif output_type == 'binary':
                output_value = bin(decimal_value)[2:]
            elif output_type == 'decimal':
                output_value = str(decimal_value)
            else:
                self.output_var.set("Hata")
                return

            self.output_var.set(output_value)

        except Exception:
            self.output_var.set("Hata")

if __name__ == "__main__":
    calculator = AdvancedCalculator()
    calculator.mainloop()
