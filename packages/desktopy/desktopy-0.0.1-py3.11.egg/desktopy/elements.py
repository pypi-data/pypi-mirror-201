from tkinter import *
from tkinter import messagebox
from tkinter import Button as TButton
from PIL import Image as PilImage
from PIL import ImageTk
import tkintermapview
import customtkinter
from tkinter.filedialog import askopenfilename


class Window():
    def __init__(self, title: str = "base window", height: int = 100, width: int = 100, icon: str = None):
        self.root: Tk = customtkinter.CTk()
        self.root.geometry(f"{width}x{height}")
        self.root.eval('tk::PlaceWindow . center')
        self.root.iconbitmap(icon)
        self.root.title(title)

    def add(self, panel: Frame, **kwargs) -> None:
        panel.add_to(self.root, **kwargs)

    def open(self) -> None:
        self.root.mainloop()

    def update_after(self, time: int, callback: callable) -> None:
        self.root.after(time, callback)

    def close(self) -> None:
        self.root.destroy()


class Panel():
    def __init__(self, variant: dict = {}, **kwargs):
        self.variant = variant
        self.layout = self.variant["display"] if "display" in self.variant else ""

    def add_to(self, root: Tk, **kwargs):
        if("as_child" in kwargs):
            self.panel = root

            self.frame: customtkinter.CTkFrame = customtkinter.CTkFrame(
                master=self.panel.frame,
                width=self.variant["width"] if "width" in self.variant else 100,
                height=self.variant["height"] if "height" in self.variant else 100,
                fg_color=self.variant["background-color"] if "background-color" in self.variant else "black",
                corner_radius=self.variant["border-radius"] if "border-radius" in self.variant else 0,
                border_width=self.variant["border-width"] if "border-width" in self.variant else 0,
                border_color=self.variant["border-color"] if "border-color" in self.variant else "black",
            )

            self.fill = None

            if "max-width" in self.variant:
                self.fill = "x"
            if "max-height" in self.variant:
                self.fill = "y"
            if ("max-width" in self.variant and "max-height" in self.variant):
                self.fill = "both"

            if (self.panel.layout != "grid"):
                self.frame.pack(fill=self.fill, expand=True)

            if ("position" in self.variant):
                if (self.variant["position"] == "absolute"):
                    self.frame.place(
                        ipadx=self.variant["padding-x"] if (
                            "padding-x") in self.variant else 0,
                        ipady=self.variant["padding-y"] if (
                            "padding-y") in self.variant else 0,
                        x=self.variant["x"], y=self.variant["y"], anchor="ne")
                if (self.variant["position"] == "relative"):
                    self.frame.place(
                        ipadx=self.variant["padding-x"] if (
                            "padding-x") in self.variant else 0,
                        ipady=self.variant["padding-y"] if (
                            "padding-y") in self.variant else 0,
                        relx=self.variant["x"], rely=self.variant["y"], anchor="ne")

            if (self.panel.layout == "grid"):
                self.frame.grid(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    padx=self.variant["margin-x"] if (
                        "margin-x") in self.variant else 0,
                    pady=self.variant["margin-y"] if (
                        "margin-y") in self.variant else 0,
                    column=self.variant["grid-column-start"],
                    row=self.variant["grid-row-start"],
                    columnspan=self.variant["grid-row-end"] if "grid-row-end" in self.variant else None,
                    rowspan=self.variant["grid-column-end"] if "grid-column-end" in self.variant else None,
                )

                if ("max-width" in self.variant and self.variant["max-width"] == "stretch"):
                    Grid.rowconfigure(self.panel.frame,
                                    self.panel.variant["grid-row"], weight=1)
                if ("max-height" in self.variant and self.variant["max-height"] == "stretch"):
                    Grid.columnconfigure(
                        self.panel.frame, self.panel.variant["grid-column"], weight=1)

            return self.frame
        self.root = root
        self.frame: customtkinter.CTkFrame = customtkinter.CTkFrame(
            self.root,
            width=self.variant["width"] if "width" in self.variant else 100,
            height=self.variant["height"] if "height" in self.variant else 100,
            fg_color=self.variant["background-color"] if "background-color" in self.variant else "black",
            corner_radius=self.variant["border-radius"] if "border-radius" in self.variant else 0,
            border_width=self.variant["border-width"] if "border-width" in self.variant else 0,
            border_color=self.variant["border-color"] if "border-color" in self.variant else "black",
        )
        if (self.layout == "none"):
            self.frame.destroy()

        self.fill = None

        if "max-width" in self.variant:
            self.fill = "x"
        if "max-height" in self.variant:
            self.fill = "y"
        if ("max-width" in self.variant and "max-height" in self.variant):
            self.fill = "both"
        if ("max-width" not in self.variant):
            self.frame.pack_propagate(False)

        if (self.layout == "grid"):
            self.frame.grid()
            if ("grid-column" in self.variant and "grid-row" in self.variant):
                self.frame.grid(
                    column=self.variant["grid-column"],
                    row=self.variant["grid-row"]
                )
            if ("max-width" not in self.variant):
                self.frame.grid_propagate(False)

        self.frame.pack(fill=self.fill, expand=True)


    def set_variant(self, variant: dict = {}):
        self.frame.destroy()
        self.variant = variant
        self.add_to(self.root)

    def add(self, component: object, **kwargs):
        component.add_to(self, **kwargs)


class Text():
    def __init__(self, text: str = "", variant: dict = {}, image: PhotoImage = None):
        self.variant = variant
        self.value = text
        self.img = image

    def add_to(self, panel: Frame, **kwargs) -> Label:
        self.panel = panel

        self.text: customtkinter.CTkLabel = customtkinter.CTkLabel(
            master=self.panel.frame,
            text=self.value,
            image=self.img,
            width=self.variant["width"] if "width" in self.variant else 100,
            height=self.variant["height"] if "height" in self.variant else 100,
            fg_color=self.variant["background-color"] if "background-color" in self.variant else "black",
            corner_radius=self.variant["border-radius"] if "border-radius" in self.variant else 0,
            text_color=self.variant["color"] if "color" in self.variant else "white",
            font=(
                self.variant["font-family"] if "font-family" in self.variant else "Helvetica",
                self.variant["font-size"] if "font-size" in self.variant else 12,
                self.variant["font-weight"] if "font-weight" in self.variant else ""
            )
        )

        self.text.image = self.img

        self.fill = None

        if "max-width" in self.variant:
            self.fill = "x"
        if "max-height" in self.variant:
            self.fill = "y"
        if ("max-width" in self.variant and "max-height" in self.variant):
            self.fill = "both"

        if (self.panel.layout != "grid"):
            self.text.pack(fill=self.fill, expand=True)

        if ("position" in self.variant):
            if (self.variant["position"] == "absolute"):
                self.text.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    x=self.variant["x"], y=self.variant["y"], anchor="ne")
            if (self.variant["position"] == "relative"):
                self.text.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    relx=self.variant["x"], rely=self.variant["y"], anchor="ne")

        if (self.panel.layout == "grid"):
            self.text.grid(
                ipadx=self.variant["padding-x"] if (
                    "padding-x") in self.variant else 0,
                ipady=self.variant["padding-y"] if (
                    "padding-y") in self.variant else 0,
                padx=self.variant["margin-x"] if (
                    "margin-x") in self.variant else 0,
                pady=self.variant["margin-y"] if (
                    "margin-y") in self.variant else 0,
                column=self.variant["grid-column-start"],
                row=self.variant["grid-row-start"],
                columnspan=self.variant["grid-row-end"] if "grid-row-end" in self.variant else None,
                rowspan=self.variant["grid-column-end"] if "grid-column-end" in self.variant else None,
            )

            if ("max-width" in self.variant and self.variant["max-width"] == "stretch"):
                Grid.rowconfigure(self.panel.frame,
                                  self.panel.variant["grid-row"], weight=1)
            if ("max-height" in self.variant and self.variant["max-height"] == "stretch"):
                Grid.columnconfigure(
                    self.panel.frame, self.panel.variant["grid-column"], weight=1)

        return self.text

    def set_text(self, value: str):
        self.text.configure(text=value)

    def set_variant(self, variant: dict = {}):
        self.text.destroy()
        self.variant = variant
        self.add_to(self.panel)

    def get_text(self):
        self.text["text"]


class TextField():
    def __init__(self, text: str = "", placeholder: str = "", variant: dict = {}):
        self.variant = variant
        self.placeholder = placeholder
        self.value = text

    def add_to(self, panel: Frame, **kwargs) -> Entry:
        self.panel = panel

        self.text_field: customtkinter.CTkEntry = customtkinter.CTkEntry(
            master=self.panel.frame,
            placeholder_text=self.placeholder,
            placeholder_text_color="grey",
            fg_color=self.variant["background-color"] if "background-color" in self.variant else "black",
            text_color=self.variant["color"] if "color" in self.variant else "white",
            corner_radius=self.variant["border-radius"] if "border-radius" in self.variant else 0,
            border_color=self.variant["border-color"] if "border-color" in self.variant else "black",
            border_width=self.variant["border-width"] if "border-width" in self.variant else 0,
            font=(
                self.variant["font-family"] if "font-family" in self.variant else "Helvetica",
                self.variant["font-size"] if "font-size" in self.variant else 12,
                self.variant["font-weight"] if "font-weight" in self.variant else ""
            )
        )

        self.text_field.insert(0, self.value)

        self.fill = None

        if "max-width" in self.variant:
            self.fill = "x"
        if "max-height" in self.variant:
            self.fill = "y"
        if ("max-width" in self.variant and "max-height" in self.variant):
            self.fill = "both"

        if (self.panel.layout != "grid"):
            self.text_field.pack(fill=self.fill, expand=True)

        if ("position" in self.variant):
            if (self.variant["position"] == "absolute"):
                self.text_field.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    x=self.variant["x"], y=self.variant["y"], anchor="ne")
            if (self.variant["position"] == "relative"):
                self.text_field.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    relx=self.variant["x"], rely=self.variant["y"], anchor="ne")

        if (self.panel.layout == "grid"):
            self.text_field.grid(
                ipadx=self.variant["padding-x"] if (
                    "padding-x") in self.variant else 0,
                ipady=self.variant["padding-y"] if (
                    "padding-y") in self.variant else 0,
                padx=self.variant["margin-x"] if (
                    "margin-x") in self.variant else 0,
                pady=self.variant["margin-y"] if (
                    "margin-y") in self.variant else 0,
                column=self.variant["grid-column-start"],
                row=self.variant["grid-row-start"],
                columnspan=self.variant["grid-row-end"] if "grid-row-end" in self.variant else None,
                rowspan=self.variant["grid-column-end"] if "grid-column-end" in self.variant else None,
            )

            if ("max-width" in self.variant and self.variant["max-width"] == "stretch"):
                Grid.rowconfigure(self.panel.frame,
                                  self.panel.variant["grid-row"], weight=1)
            if ("max-height" in self.variant and self.variant["max-height"] == "stretch"):
                Grid.columnconfigure(
                    self.panel.frame, self.panel.variant["grid-column"], weight=1)

        return self.text_field

    def set_text(self, value: str):
        self.text_field.insert(0, value)

    def set_variant(self, variant: dict = {}):
        self.text_field.destroy()
        self.variant = variant
        self.add_to(self.panel)

    def get_text(self):
        return self.text_field.get()

    def set_state(self, state: str = "normal"):
        self.text_field.configure(state=state)


class Button():
    def __init__(self, text: str = "", variant: dict = {}):
        self.variant = variant
        self.value = text

    def add_to(self, panel: Panel, **kwargs) -> Entry:
        self.panel = panel

        self.button: customtkinter.CTkButton = customtkinter.CTkButton(
            master=self.panel.frame,
            text=self.value,
            width=self.variant["width"] if (
                "width" in self.variant and self.variant["width"] != "fill") else 100,
            height=self.variant["height"] if (
                "height" in self.variant and self.variant["height"] != "fill") else 100,
            fg_color=self.variant["background-color"] if "background-color" in self.variant else "black",
            text_color=self.variant["color"] if "color" in self.variant else "white",
            corner_radius=self.variant["border-radius"] if "border-radius" in self.variant else 0,
            border_width=self.variant["border-width"] if "border-width" in self.variant else 0,
            border_color=self.variant["border-color"] if "border-color" in self.variant else "black",
            hover_color=self.variant["background-color:hover"] if "background-color:hover" in self.variant else "grey",
            hover=True,
            font=(
                self.variant["font-family"] if "font-family" in self.variant else "Helvetica",
                self.variant["font-size"] if "font-size" in self.variant else 12,
                self.variant["font-weight"] if "font-weight" in self.variant else ""
            )
        )

        self.fill = None

        if "max-width" in self.variant:
            self.fill = "x"
        if "max-height" in self.variant:
            self.fill = "y"
        if ("max-width" in self.variant and "max-height" in self.variant):
            self.fill = "both"

        if (self.panel.layout != "grid"):
            self.button.pack(fill=self.fill, expand=True)

        if ("position" in self.variant):
            if (self.variant["position"] == "absolute"):
                self.button.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    x=self.variant["x"], y=self.variant["y"], anchor="ne")
            if (self.variant["position"] == "relative"):
                self.button.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    relx=self.variant["x"], rely=self.variant["y"], anchor="ne")

        if (self.panel.layout == "grid"):
            self.button.grid(
                ipadx=self.variant["padding-x"] if (
                    "padding-x") in self.variant else 0,
                ipady=self.variant["padding-y"] if (
                    "padding-y") in self.variant else 0,
                padx=self.variant["margin-x"] if (
                    "margin-x") in self.variant else 0,
                pady=self.variant["margin-y"] if (
                    "margin-y") in self.variant else 0,
                column=self.variant["grid-column-start"],
                row=self.variant["grid-row-start"],
                columnspan=self.variant["grid-row-end"] if "grid-row-end" in self.variant else None,
                rowspan=self.variant["grid-column-end"] if "grid-column-end" in self.variant else None,
            )

            if ("max-width" in self.variant and self.variant["max-width"] == "stretch"):
                Grid.rowconfigure(self.panel.frame,
                                  self.panel.variant["grid-row"], weight=1)
            if ("max-height" in self.variant and self.variant["max-height"] == "stretch"):
                Grid.columnconfigure(
                    self.panel.frame, self.panel.variant["grid-column"], weight=1)

        return self.button

    def set_state(self, state: str = "normal"):
        self.button.configure(state=state)

    def set_text(self, value: str):
        self.button.insert(0, value)

    def set_variant(self, variant: dict = {}):
        self.button.destroy()
        self.variant = variant
        self.add_to(self.panel)

    def get_text(self):
        return self.button.get()

    def on_click(self, callback: callable):
        self.button.bind('<Button-1>', callback)

    def on_right_click(self, callback: callable):
        self.button.bind('<Button-3>', callback)

    def on_scroll_click(self, callback: callable):
        self.button.bind('<Button-2>', callback)

    def on_double_click(self, callback: callable):
        self.button.bind('<Double-Button-1>', callback)

    def on_double_right_click(self, callback: callable):
        self.button.bind('Double-Button-3', callback)

    def on_mouse_over(self, callback: callable):
        self.button.bind('<Enter>', callback)

    def on_mouse_leave(self, callback: callable):
        self.button.bind('<Leave>', callback)

    def on_key_press(self, callback: callable):
        self.button.bind('<KeyPress>', callback)

    def on_key_release(self, callback: callable):
        self.button.bind('<KeyRelease>', callback)

    def press_enter(self, callback: callable):
        self.button.bind('<Return>', callback)

    def press_back(self, callback: callable):
        self.button.bind('<Return>', callback)


class Image():
    def __init__(self, path: str, variant: dict = {}):
        self.path = path
        self.variant = variant

    def add_to(self, panel: Frame, **kwargs):
        self.img_file = PilImage.open(self.path)
        self.img_file = self.img_file.resize((
            self.variant["width"] if "width" in self.variant else 100,
            self.variant["height"] if "height" in self.variant else 100
        ), PilImage.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img_file)
        self.label = Text(image=self.img, variant=self.variant)
        self.label.add_to(panel)
        # panel.create_image(
        #     self.variant["height"],
        #     self.variant["width"],
        #     image=self.img
        # )


class MessageBox():
    @staticmethod
    def ask(title=None, message=None):
        messagebox.askyesnocancel(title, message)

    @staticmethod
    def info(title=None, message=None):
        messagebox.showinfo(title, message)

    @staticmethod
    def warning(title=None, message=None):
        messagebox.showwarning(title, message)

    @staticmethod
    def error(title=None, message=None):
        messagebox.showerror(title, message)


class Map():
    waypoints: list = []

    def __init__(self, width=800, height=600, corner_radius=0, variant={}, database_path=None):
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.variant = variant
        self.use_database_only = False
        self.database_path = database_path
        if (database_path != None):
            self.use_database_only = True

    def get_map(self):
        return self.map

    def add_to(self, panel: Panel, **kwargs):
        self.panel = panel
        self.map = tkintermapview.TkinterMapView(
            self.panel.frame,
            width=self.width,
            height=self.height,
            bg_color="black",
            corner_radius=self.corner_radius,
            database_path=self.database_path,
            use_database_only=self.use_database_only
        )

        self.fill = None

        if "max-width" in self.variant:
            self.fill = "x"
        if "max-height" in self.variant:
            self.fill = "y"
        if ("max-width" in self.variant and "max-height" in self.variant):
            self.fill = "both"

        if (self.panel.layout != "grid"):
            self.map.pack(fill=self.fill, expand=True)

        if ("position" in self.variant):
            if (self.variant["position"] == "absolute"):
                self.map.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    x=self.variant["x"], y=self.variant["y"], anchor="ne")
            if (self.variant["position"] == "relative"):
                self.map.place(
                    ipadx=self.variant["padding-x"] if (
                        "padding-x") in self.variant else 0,
                    ipady=self.variant["padding-y"] if (
                        "padding-y") in self.variant else 0,
                    relx=self.variant["x"], rely=self.variant["y"], anchor="ne")

        if (self.panel.layout == "grid"):
            self.map.grid(

                ipadx=self.variant["padding-x"] if (
                    "padding-x") in self.variant else 0,
                ipady=self.variant["padding-y"] if (
                    "padding-y") in self.variant else 0,
                padx=self.variant["margin-x"] if (
                    "margin-x") in self.variant else 0,
                pady=self.variant["margin-y"] if (
                    "margin-y") in self.variant else 0,
                column=self.variant["grid-column-start"],
                row=self.variant["grid-row-start"],
                columnspan=self.variant["grid-row-end"] if "grid-row-end" in self.variant else None,
                rowspan=self.variant["grid-column-end"] if "grid-column-end" in self.variant else None,
            )

            if ("max-width" in self.variant and self.variant["max-width"] == "stretch"):
                Grid.rowconfigure(self.panel.frame,
                                  self.panel.variant["grid-row"], weight=1)
            if ("max-height" in self.variant and self.variant["max-height"] == "stretch"):
                Grid.columnconfigure(
                    self.panel.frame, self.panel.variant["grid-column"], weight=1)

    def clear_path(self):
        self.map.delete()

    def add_waypoint(self, waypoint: tuple = ()):
        self.map.set_marker(waypoint[0], waypoint[1])
        self.waypoints.append((waypoint[0], waypoint[1]))
        self.map.set_path(self.waypoints)

    def remove_waypoint(self, waypoint: tuple = ()):
        self.map.remove_position(waypoint)

    def set_marker(self, latitude, longtitude, label=""):
        self.map.set_position(latitude, longtitude)
        self.map.set_zoom(15)
        return self.map.set_marker(latitude, longtitude, text=label)

    def on_click(self, callback: callable):
        self.map.add_left_click_map_command(callback)

    def on_right_click(self, label: str, callback: callable):
        self.map.add_right_click_menu_command(
            label=label,
            command=callback,
            pass_coords=True
        )

    def set_tile_map(self, tile_map: str):
        if (tile_map == "google maps"):
            self.map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

        if (tile_map == "google maps satellite"):
            self.map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

        if (tile_map == "no labels"):
            self.map.set_tile_server(
                "https://tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png")  # no labels


class Camera():
    pass


class FileChooser():
    def open(self):
        self.window = Window(title="Choose A File")
        file = askopenfilename()
        self.window.close()
        return file
