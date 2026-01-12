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
# Prepare root grid with two columns for later layouts
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(5, weight=1) #Spacer
style = ttk.Style(root)
style.configure('Large.TButton', font=('TkDefaultFont', 12), padding=6)

canvas = None
j = 1j
RC_invert = False
LR_invert = False
rc_status_label = None
lr_status_label = None

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def toggle_RC_invert():
    global RC_invert, rc_status_label
    RC_invert = not RC_invert
    if rc_status_label is not None:
        rc_status_label.config(text="On" if RC_invert else "Off", fg="green" if RC_invert else "red")

def toggle_LR_invert():
    global LR_invert, lr_status_label
    LR_invert = not LR_invert
    if lr_status_label is not None:
        lr_status_label.config(text="On" if LR_invert else "Off", fg="green" if LR_invert else "red")

def main_menu():
    clear_frame()
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.rowconfigure(5, weight=1) #Spacer

    ttk.Button(root, text="RC Circuit", command=RC_Circuit, style='Large.TButton', width=20).grid(row=1, column=0, columnspan=2, pady=10)
    ttk.Button(root, text="LR Circuit", command=LR_Circuit, style='Large.TButton', width=20).grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(root, text="RLC Circuit", command=RLC_Circuit, style='Large.TButton', width=20).grid(row=3, column=0, columnspan=2, pady=10)

def RC_Circuit():
    clear_frame()
    global RC_invert, left_frame, right_frame, fc_var, rc_status_label

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.rowconfigure(5, weight=1) #Spacer

    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Controls on the left
    resistance_input = tk.Label(left_frame, text="Enter Resistance (R) in Ohms:")
    resistance_input.pack(pady=5)
    entry1 = tk.Entry(left_frame)
    entry1.pack(pady=5)
    capacitance_input = tk.Label(left_frame, text="Enter Capacitance (C) in Farads:")
    capacitance_input.pack(pady=5)
    entry2 = tk.Entry(left_frame)
    entry2.pack(pady=5)
    ttk.Button(left_frame, text="Plot RC Circuit", command=lambda: plot_RC(entry1, entry2)).pack(pady=20)
    label_info = tk.Label(left_frame, text="Switch from RC -> CR and vice versa:").pack(pady=5)
    toggle_frame = tk.Frame(left_frame)
    toggle_frame.pack(pady=5)
    ttk.Button(toggle_frame, text="Toggle Invert/Non-Invert", command=lambda: toggle_RC_invert()).pack(side='left', padx=(0,10))
    rc_status_label = tk.Label(toggle_frame, text=("On" if RC_invert else "Off"), fg=("green" if RC_invert else "red"))
    rc_status_label.pack(side='left')
    ttk.Button(left_frame, text="Back to Main Menu", command=lambda: main_menu()).pack(pady=20)

    # Info on the right
    fc_var = tk.StringVar(value="Cutoff Frequency: __ Hz")
    tk.Label(right_frame, textvariable=fc_var, font=("TkDefaultFont", 12)).pack(pady=5) 

def plot_RC(entry1, entry2):
    if not entry1.get() or not entry2.get():
        return
    
    global canvas
    global RC_invert, right_frame, fc_var
    R = float(entry1.get())
    C = float(entry2.get())

    wc = 1/(R*C)
    fc = wc/(2*np.pi)
    w = np.logspace(0, 8, num=500)

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
    ax1.set_title('Transfer Function')
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

    fc_var.set(f"Cutoff Frequency: {fc:.2f} Hz")
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) 

def LR_Circuit():
    clear_frame()
    
    global LR_invert, left_frame, right_frame, fc_var, lr_status_label

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.rowconfigure(5, weight=1) #Spacer

    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Controls on the left
    inductance_input = tk.Label(left_frame, text="Enter Inductance (L) in Henries:")
    inductance_input.pack(pady=5)
    entry1 = tk.Entry(left_frame)
    entry1.pack(pady=5)
    resistance_input = tk.Label(left_frame, text="Enter Resistance (R) in Ohms:")
    resistance_input.pack(pady=5)
    entry2 = tk.Entry(left_frame)
    entry2.pack(pady=5)
    ttk.Button(left_frame, text="Plot LR Circuit", command=lambda: plot_LR(entry1, entry2)).pack(pady=20)
    label_info = tk.Label(left_frame, text="Switch from LR -> RL and vice versa:").pack(pady=5)
    toggle_frame = tk.Frame(left_frame)
    toggle_frame.pack(pady=5)
    ttk.Button(toggle_frame, text="Toggle Invert/Non-Invert", command=lambda: toggle_LR_invert()).pack(side='left', padx=(0,10))
    lr_status_label = tk.Label(toggle_frame, text=("On" if LR_invert else "Off"), fg=("green" if LR_invert else "red"))
    lr_status_label.pack(side='left')
    ttk.Button(left_frame, text="Back to Main Menu", command=lambda: main_menu()).pack(pady=20)

    # Info on the right
    fc_var = tk.StringVar(value="Cutoff Frequency: __ Hz")
    tk.Label(right_frame, textvariable=fc_var, font=("TkDefaultFont", 12)).pack(pady=5) 

def plot_LR(entry1, entry2):
    if not entry1.get() or not entry2.get():
        return
    
    global canvas
    global LR_invert, right_frame, fc_var
    L = float(entry1.get())
    R = float(entry2.get())

    wc = R/L
    fc = wc/(2*np.pi)
    w = np.logspace(0, 8, num=500)

    if LR_invert:
        H = (j*w*L)/(R + j*w*L)
    else:
        H = R/(R + j*w*L)

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    fig = Figure(figsize=(8, 5), dpi=100)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.semilogx(w/(2*np.pi), 20*np.log10(np.abs(H)))
    ax1.set_title('Transfer Function')
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

    fc_var.set(f"Cutoff Frequency: {fc:.2f} Hz")
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def RLC_Circuit():
    clear_frame()
    
    global left_frame, right_frame, fc_var1, fc_var2, bandwidth_var, q_factor_var

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.rowconfigure(5, weight=1) #Spacer

    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Controls on the left
    resistance_input = tk.Label(left_frame, text="Enter Resistance (R) in Ohms:")
    resistance_input.pack(pady=5)
    entry1 = tk.Entry(left_frame)
    entry1.pack(pady=5)
    capacitance_input = tk.Label(left_frame, text="Enter Capacitance (C) in Farads:")
    capacitance_input.pack(pady=5)
    entry2 = tk.Entry(left_frame)
    entry2.pack(pady=5)
    inductance_input = tk.Label(left_frame, text="Enter Inductance (L) in Henries:")
    inductance_input.pack(pady=5)
    entry3 = tk.Entry(left_frame)
    entry3.pack(pady=5)
    ttk.Button(left_frame, text="Plot RLC Circuit", command=lambda: plot_RLC(entry1, entry2, entry3)).pack(pady=20)
    toggle_frame = tk.Frame(left_frame)
    toggle_frame.pack(pady=5)
    ttk.Button(left_frame, text="Back to Main Menu", command=lambda: main_menu()).pack(pady=20)

    # Info on the right
    fc_var1 = tk.StringVar(value="Lower Cutoff Frequency: __ Hz")
    tk.Label(right_frame, textvariable=fc_var1, font=("TkDefaultFont", 12)).pack(pady=5)
    fc_var2 = tk.StringVar(value="Higher Cutoff Frequency: __ Hz")
    tk.Label(right_frame, textvariable=fc_var2, font=("TkDefaultFont", 12)).pack(pady=5)
    bandwidth_var = tk.StringVar(value="Bandwidth: __ Hz")
    tk.Label(right_frame, textvariable=bandwidth_var, font=("TkDefaultFont", 12)).pack(pady=5)
    q_factor_var = tk.StringVar(value="Q Factor: __")
    tk.Label(right_frame, textvariable=q_factor_var, font=("TkDefaultFont", 12)).pack(pady=5)

def plot_RLC(entry1, entry2, entry3):
    if not entry1.get() or not entry2.get() or not entry3.get():
        return
    
    global canvas
    global right_frame, fc_var1, fc_var2, bandwidth_var, q_factor_var
    R = float(entry1.get())
    C = float(entry2.get())
    L = float(entry3.get())

    wc0 = 1/np.sqrt(L*C)
    Q = (1/R)*np.sqrt(L/C)
    wc1 = np.sqrt((R/(2*L))**2 + 1/(L*C)) - R/(2*L)
    wc2 = np.sqrt((R/(2*L))**2 + 1/(L*C)) + R/(2*L)
    bw = (wc2 - wc1)/(2*np.pi)
    fc1 = wc1/(2*np.pi)
    fc2 = wc2/(2*np.pi)
    w = np.logspace(0, 8, num=500)

    H = R/((1/(j*w*C)) + j*w*L + R)

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    fig = Figure(figsize=(8, 5), dpi=100)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.semilogx(w/(2*np.pi), 20*np.log10(np.abs(H)))
    ax1.set_title('Transfer Function')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.grid(True, which='both')
    ax1.axvline(fc1, color='red', linestyle='--', label='Lower Cutoff Frequency')
    ax1.axvline(fc2, color='green', linestyle='--', label='Higher Cutoff Frequency')
    ax1.legend()

    ax2.semilogx(w/(2*np.pi), np.angle(H, deg=True))
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.grid(True, which='both')
    ax2.axvline(fc1, color='red', linestyle='--', label='Lower Cutoff Frequency')
    ax2.axvline(fc2, color='green', linestyle='--', label='Higher Cutoff Frequency')
    ax2.legend()
    fc_var1.set(f"Lower Cutoff Frequency: {fc1:.2f} Hz")
    fc_var2.set(f"Higher Cutoff Frequency: {fc2:.2f} Hz")
    bandwidth_var.set(f"Bandwidth: {bw/(2*np.pi):.2f} Hz")
    q_factor_var.set(f"Q Factor: {Q:.2f}")

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ttk.Button(root, text="RC Circuit", command=RC_Circuit, style='Large.TButton', width=20).grid(row=1, column=0, columnspan=2, pady=10)
ttk.Button(root, text="LR Circuit", command=LR_Circuit, style='Large.TButton', width=20).grid(row=2, column=0, columnspan=2, pady=10)
ttk.Button(root, text="RLC Circuit", command=RLC_Circuit, style='Large.TButton', width=20).grid(row=3, column=0, columnspan=2, pady=10)
root.mainloop()
