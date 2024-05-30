import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#[2]
def abrirArch():

    global ruta
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")])
    
    if ruta:
        messagebox.showinfo("Archivo Seleccionado", f"El archivo seleccionado: {ruta}")
        btnBorrarDatos.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Error", "No se selecciono ningun archivo")
        btnBorrarDatos.config(state=tk.DISABLED)

#[3]
def eliminar():
    nombre, extension = os.path.splitext(os.path.basename(ruta))
    
    #[4]
    if extension == ".pdf":
        try:
            archivo_salida = 'reparado_' + nombre
        
            subprocess.run(['qpdf', '--linearize', ruta, archivo_salida], check=True)

            with open(archivo_salida, 'ab') as file:
                file.write(''.encode('utf-8'))
        
            print(f"El contenido posterior al EOF ha sido eliminado y se ha añadido nuevo contenido en {archivo_salida}")

        except subprocess.CalledProcessError as e:
            print(f"Error al procesar el archivo con qpdf: {e}")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
    
    elif extension == '.jpeg' or extension == '.jpg':
        archivos(b'\xFF\xD9')

    elif extension == '.png':
        archivos(b'\x49\x45\x4E\x44\xAE\x42\x60\x82')
    
    elif extension == '.gif':
        archivos(b'\x3B')

    elif extension == '.html':
        archivos(b'</html>')
        
    elif extension == '.docx' or extension == '.pptx':
        
        archivos(b'\x00\x00\x00')

    elif extension == '.zip':
        archivosZip()

#[5]    
def archivos(marcadorEOF):
    try:
        with open(ruta, 'rb') as file:
            contenido = file.read()
        
        #[6]
        eof_index = contenido.rfind(marcadorEOF)
        
        if eof_index == -1:
            print(f"No se encontró el marcador de fin de archivo para {ruta}.")
            return
        
        #[7]
        eof_index += len(marcadorEOF)
        print(eof_index)
        
        contenido_valido = contenido[:eof_index]
        
        #[8]
        with open(ruta, 'wb') as file:
            file.write(contenido_valido)
        
        if file:
            messagebox.showinfo("Exito", f"El contenido posterior al EOF ha sido eliminado en {ruta}")
        else:
            messagebox.showerror("Error", f"El contenido posterior al EOF ha sido eliminado en {ruta}")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

#[9]
def archivosZip():
    try:
        with open(ruta, 'rb') as file:
            contenido = file.read()

        eocd_signature = b'\x50\x4b\x05\x06'
        eocd_index = contenido.rfind(eocd_signature)

        if eocd_index == -1:
            messagebox.showerror("Error", "No se encontró el EOCD en el archivo ZIP.")
            return

        contenido_valido = contenido[:eocd_index + 22]
        with open(ruta, 'wb') as file:
            file.write(contenido_valido)

        messagebox.showinfo("Éxito", f"El contenido posterior al EOCD ha sido eliminado en {ruta}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el archivo ZIP: {e}")

#[1]
ventana = tk.Tk()
ventana.title("Borrar despues del EOF")
ventana.geometry("300x200")
ruta = ""

btnAbrir = tk.Button(ventana, text="Abrir Archivo", command=abrirArch)
btnAbrir.pack(padx=30, pady=20)

btnBorrarDatos = tk.Button(ventana, text="Borrar Datos", command=eliminar, state=tk.DISABLED)
btnBorrarDatos.pack(padx=30, pady=10)

ventana.mainloop()