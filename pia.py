import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador Financiero - Método Bola de Nieve")
        self.root.geometry("600x400")
        
        # Variables principales
        self.num_tarjetas = tk.StringVar(value="0")
        self.sueldo_mensual = tk.StringVar(value="0.0")
        self.gastos_basicos = tk.StringVar(value="0.0")
        self.tarjetas_info = []
        
        # Frame inicial
        self.inicial_frame()

    def inicial_frame(self):
        self.limpiar_ventana()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="📋 Bienvenido al Planificador Financiero", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(frame, text="Por favor, indica cuántas tarjetas de crédito tienes con saldo pendiente:", font=("Arial", 12)).pack()
        tk.Entry(frame, textvariable=self.num_tarjetas, font=("Arial", 12)).pack(pady=5)
        tk.Button(frame, text="Continuar ➡️", command=self.ingresar_datos_tarjetas, font=("Arial", 12)).pack(pady=10)

    def ingresar_datos_tarjetas(self):
        if not self.num_tarjetas.get().isdigit():
            messagebox.showerror("Error", "Solo se aceptan caracteres numéricos.")
            return

        self.num_tarjetas_val = int(self.num_tarjetas.get())
        if self.num_tarjetas_val < 1:
            messagebox.showerror("Error", "Debes ingresar al menos una tarjeta.")
            return

        self.limpiar_ventana()
        self.tarjetas_info.clear()

        tk.Label(self.root, text="🔢 Datos de tus Tarjetas", font=("Arial", 14, "bold")).pack(pady=10)

        for i in range(self.num_tarjetas_val):
            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=5)

            saldo = tk.StringVar(value="0.0")
            pago_minimo = tk.StringVar(value="0.0")
            self.tarjetas_info.append((saldo, pago_minimo))

            tk.Label(frame, text=f"Tarjeta {i+1} - Saldo:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
            tk.Entry(frame, textvariable=saldo, font=("Arial", 12)).grid(row=0, column=1, padx=5)
            tk.Label(frame, text="Pago Mínimo:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
            tk.Entry(frame, textvariable=pago_minimo, font=("Arial", 12)).grid(row=0, column=3, padx=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="📊 Salario mensual:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.sueldo_mensual, font=("Arial", 12)).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="💰 Gastos básicos mensuales:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.gastos_basicos, font=("Arial", 12)).grid(row=1, column=1, padx=5)

        tk.Button(frame, text="Calcular Recomendaciones ✅", command=self.validar_entradas, font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=10)

    def validar_entradas(self):
        for saldo, pago_minimo in self.tarjetas_info:
            if not saldo.get().isdigit() or not pago_minimo.get().isdigit():
                messagebox.showerror("Error", "Solo se aceptan caracteres numéricos.")
                return

        if not self.sueldo_mensual.get().isdigit() or not self.gastos_basicos.get().isdigit():
            messagebox.showerror("Error", "Solo se aceptan caracteres numéricos.")
            return
        
        self.calcular_recomendaciones()

    def calcular_recomendaciones(self):
        tarjetas = []
        for saldo, pago_minimo in self.tarjetas_info:
            tarjetas.append({
                'saldo': float(saldo.get()),
                'pago_minimo': float(pago_minimo.get())
            })

        sueldo = float(self.sueldo_mensual.get())
        gastos = float(self.gastos_basicos.get())
        restante = sueldo - gastos
        fondo_emergencia = restante * 0.25
        disponible_para_deuda = restante - fondo_emergencia

        resultado = f"🛡️ Fondo de emergencia (25%): ${fondo_emergencia:.2f}\n"
        resultado += f"💳 Disponible para deudas: ${disponible_para_deuda:.2f}\n\n"

        recomendaciones = self.plan_bola_de_nieve(tarjetas, disponible_para_deuda)
        resultado += recomendaciones

        messagebox.showinfo("Recomendaciones de Pago", resultado)

    def plan_bola_de_nieve(self, tarjetas, disponible_para_deuda):
        recomendaciones = ""
        while any(tarjeta['saldo'] > 0 for tarjeta in tarjetas):
            tarjetas_ordenadas = sorted(tarjetas, key=lambda x: x['saldo'])
            deuda_restante = disponible_para_deuda

            for tarjeta in tarjetas_ordenadas:
                if tarjeta['saldo'] > 0:
                    pago_recomendado = min(deuda_restante, tarjeta['pago_minimo'], tarjeta['saldo'])
                    recomendaciones += f"  - Pagar ${pago_recomendado:.2f} a la tarjeta con saldo ${tarjeta['saldo']:.2f}\n"
                    tarjeta['saldo'] -= pago_recomendado
                    deuda_restante -= pago_recomendado

                if deuda_restante <= 0:
                    break

        if all(t['saldo'] == 0 for t in tarjetas):
            recomendaciones += "\n🎉 ¡Todas las tarjetas están pagadas!"
        else:
            recomendaciones += "\n🔄 Continuar con el siguiente mes para reducir más deuda."

        return recomendaciones

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicia el programa
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
