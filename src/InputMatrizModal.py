import tkinter as tk


class InputMatrizModal():

    def openModal(self):
        self.window = tk.Tk()
        self.window.eval('tk::PlaceWindow . center')
        self.name_matrix = None
        self.window.protocol("WM_DELETE_WINDOW", self.closeModal)
        self.window.title('Cargar matriz')

        self.label = tk.Label(
            self.window, text='Ingresa el nombre de la matriz', font=("default", 12))

        self.label.grid(column=0, row=0, columnspan=2)

        self.input = tk.Entry(self.window, font=("default", 20))
        self.input.config(width=25)
        self.input.grid(column=0, row=1, columnspan=2)

        self.confirm_button = tk.Button(
            self.window, text='Cargar', background='#bebebe', borderwidth=0, activebackground='#b3b7c0', font=("default", 12), command=self.uploadHandler)
        self.confirm_button.config(width=20, height=3)

        self.abort_button = tk.Button(
            self.window, text='Cancelar', background='#bebebe', borderwidth=0, activebackground='#b3b7c0', font=("default", 12), command=self.closeModal)
        self.abort_button.config(width=20, height=3)

        self.confirm_button.grid(column=0, row=2, pady=10, padx=10)
        self.abort_button.grid(column=1, row=2, pady=10, padx=10)

        self.window.mainloop()
        return self.name_matrix

    def uploadHandler(self):
        self.name_matrix = self.input.get()
        self.closeModal()

    def closeModal(self):
        self.window.destroy()
