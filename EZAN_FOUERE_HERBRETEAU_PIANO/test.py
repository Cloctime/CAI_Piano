import tkinter as tk

if __name__ == "__main__":
    mw=tk.Tk()
    mw.title("Men")
    names=["Jean", "John", "Joe"]
    model = Model(names)
    view = View(mw)
    view.update(model)
    model.attach(view)
    ctrl = Controller(model,view)
