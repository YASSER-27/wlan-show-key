import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def get_wifi_list():
    """جلب قائمة بأسماء شبكات الوايفاي المحفوظة"""
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore")
        profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
        return profiles
    except Exception as e:
        return []

def get_wifi_password():
    """جلب كلمة المرور للشبكة المختارة"""
    ssid = wifi_combo.get()
    if not ssid:
        messagebox.showwarning("تنبيه", "يرجى اختيار شبكة أولاً")
        return

    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear']).decode('utf-8', errors="ignore")
        results = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
        
        if results:
            password_var.set(results[0])
        else:
            password_var.set("لا توجد كلمة سر (شبكة مفتوحة)")
    except Exception:
        messagebox.showerror("خطأ", "تعذر جلب كلمة المرور")

def copy_to_clipboard():
    """نسخ كلمة المرور إلى الحافظة"""
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    messagebox.showinfo("تم", "تم نسخ كلمة المرور بنجاح!")

# إعداد النافذة الرئيسية
root = tk.Tk()
root.title("Wi-Fi Key Finder")
root.geometry("400x300")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", padding=5, font=("Segoe UI", 10))

# الواجهة الرسومية
frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="اختر شبكة الوايفاي:", font=("Segoe UI", 10, "bold")).pack(pady=5)

wifi_list = get_wifi_list()
wifi_combo = ttk.Combobox(frame, values=wifi_list, state="readonly", width=30)
wifi_combo.pack(pady=10)

show_btn = ttk.Button(frame, text="إظهار كلمة المرور", command=get_wifi_password)
show_btn.pack(pady=5)

password_var = tk.StringVar(value="********")
pass_entry = ttk.Entry(frame, textvariable=password_var, justify="center", font=("Consolas", 12), state="readonly")
pass_entry.pack(pady=10, fill="x")

copy_btn = ttk.Button(frame, text="نسخ الكلمة", command=copy_to_clipboard)
copy_btn.pack(pady=5)

root.mainloop()