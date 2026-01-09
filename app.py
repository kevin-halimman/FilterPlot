import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

root = tk.Tk()
root.title("Filter Transfer Function Visualization")
root.geometry("1200x700")
canvas = None
j = 1j
RC_invert = False


def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def toggle_RC_invert():
    global RC_invert
    RC_invert = not RC_invert
    #RC_Circuit()

def RC_Circuit():
    clear_frame()
    global RC_invert

    resistance_input = tk.Label(root, text="Enter Resistance (R) in Ohms:")
    resistance_input.pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)
    capacitance_input = tk.Label(root, text="Enter Capacitance (C) in Farads:")
    capacitance_input.pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)
    ttk.Button(root, text="Plot RC Circuit", command=lambda: plot_RC(entry1, entry2)).pack(pady=20)
    label_info = tk.Label(root, text="Switch from RC -> CR and vice versa:").pack(pady=5)
    ttk.Button(root, text="Toggle Invert/Non-Invert", command=lambda: toggle_RC_invert()).pack(pady=5)

def plot_RC(entry1, entry2):
    if not entry1.get() or not entry2.get():
        return
    
    global canvas
    global RC_invert
    R = float(entry1.get())
    C = float(entry2.get())

    wc = 1/(R*C)
    fc = wc/(2*np.pi)
    w = np.logspace(1, 6, num=500)

    if RC_invert:
        H = R/(R + 1/(j*w*C))
    else:
        H = (1/(j*w*C))/(R + 1/(j*w*C))

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    fig = Figure(figsize=(8, 5), dpi=100)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.semilogx(w/(2*np.pi), 20*np.log10(np.abs(H)))
    ax1.set_title('RC Circuit Transfer Function')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.grid(True, which='both')
    ax1.axvline(fc, color='red', linestyle='--', label='Cutoff Frequency')
    ax1.legend()

    ax2.semilogx(w/(2*np.pi), np.angle(H, deg=True))
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.grid(True, which='both')
    ax2.axvline(fc, color='red', linestyle='--', label='Cutoff Frequency')
    ax2.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ttk.Button(root, text = "RC Circuit", command = RC_Circuit).pack()
ttk.Button(root, text = "Exit", command = root.destroy).pack(pady=10)
root.mainloop()
