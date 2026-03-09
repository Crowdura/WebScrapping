from playwright.sync_api import Error, WebError
from tkinter import messagebox
def anotExceptionRaisenScrapp(func):
    
    def wrapper(*args):
        try:
            func(*args)
        except Exception as e:
            messagebox.showerror(
                title="Error",
                message= f"Ocurrió un problema al procesar la solicitud. {e}"
            )
            print(f"Error 1 {e}")
        except Error as es:
            print(f"Error 1 {es}")
        except WebError as we:
            print(f"Error 1 {we}")
        except:
            pass
    return wrapper