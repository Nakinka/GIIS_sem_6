import tkinter as tk
import math

class GraphicalEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack()

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(fill=tk.X, pady=5)

        self.size1_entry = self.create_label_input("Радиус / a:", 100)
        self.size2_frame, self.size2_entry = self.create_optional_label_input("Высота / b:", 50)

        self.figure_type = "circle"
        self.create_figure_buttons()

        self.clear_button = tk.Button(self.control_frame, text="Очистить холст", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(self.control_frame, text="Назад", command=self.close_window)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.update_input_fields()

    def create_label_input(self, text, default):
        frame = tk.Frame(self.control_frame)
        frame.pack(side=tk.LEFT, padx=5)
        label = tk.Label(frame, text=text)
        label.pack()
        entry = tk.Entry(frame, width=5)
        entry.insert(0, str(default))
        entry.pack()
        return entry

    def create_optional_label_input(self, text, default):
        frame = tk.Frame(self.control_frame)
        label = tk.Label(frame, text=text)
        label.pack()
        entry = tk.Entry(frame, width=5)
        entry.insert(0, str(default))
        entry.pack()
        return frame, entry

    def create_figure_buttons(self):
        figures = [("Окружность", "circle"), 
                   ("Эллипс", "ellipse"), 
                   ("Гипербола", "hyperbola"), 
                   ("Парабола", "parabola")]
        for text, figure in figures:
            self.create_button(text, lambda f=figure: self.set_figure(f))

    def create_button(self, text, command):
        button = tk.Button(self.control_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5)

    def set_figure(self, figure):
        self.figure_type = figure
        self.update_input_fields()

    def update_input_fields(self):
        if self.figure_type == "circle" or self.figure_type == "parabola":
            self.size2_frame.pack_forget()
        else:
            self.size2_frame.pack(side=tk.LEFT, padx=5)

    def clear_canvas(self):
        self.canvas.delete("all")

    def close_window(self):
        self.root.quit()

    def get_sizes(self):
        try:
            size1 = int(self.size1_entry.get())
            size2 = int(self.size2_entry.get()) if self.figure_type != "circle" else size1
        except ValueError:
            size1, size2 = 100, 50
        return size1, size2

    def on_canvas_click(self, event):
        size1, size2 = self.get_sizes()
        draw_methods = {
            "circle": self.draw_circle,
            "ellipse": self.draw_ellipse,
            "hyperbola": self.draw_hyperbola,
            "parabola": self.draw_parabola
        }
        if self.figure_type == "parabola":
            draw_methods[self.figure_type](event.x, event.y, size1)
        else:
            draw_methods[self.figure_type](event.x, event.y, size1, size2)
    

    def draw_point(self, x, y, color="black"):
        self.canvas.create_oval(x, y, x+1, y+1, fill=color)
        print(f"{self.figure_type.capitalize()}: (x={x}, y={y})")

    def draw_circle(self, x0, y0, radius, _):
        step = 1 / radius
        for theta in range(0, int(2 * math.pi / step)):
            theta *= step
            x = x0 + radius * math.cos(theta)
            y = y0 + radius * math.sin(theta)
            self.root.after(int(theta * 100), self.draw_point, x, y) 

    def draw_ellipse(self, x0, y0, a, b):
        def plot_ellipse_4_points(cx, cy, x, y):
            self.root.after(100, self.draw_point, cx + x, cy + y)
            self.root.after(100, self.draw_point, cx - x, cy + y)
            self.root.after(100, self.draw_point, cx - x, cy - y)
            self.root.after(100, self.draw_point, cx + x, cy - y)

        twoASquare = 2 * a * a
        twoBSquare = 2 * b * b
        x = a
        y = 0
        xchange = b * b * (1 - 2 * a)
        ychange = a * a
        ellipseError = 0
        stoppingX = twoBSquare * a
        stoppingY = 0

        while stoppingX >= stoppingY:
            plot_ellipse_4_points(x0, y0, x, y)
            y += 1
            stoppingY += twoASquare
            ellipseError += ychange
            ychange += twoASquare

            if (2 * ellipseError + xchange) > 0:
                x -= 1
                stoppingX -= twoBSquare
                ellipseError += xchange
                xchange += twoBSquare

        x = 0
        y = b
        xchange = b * b
        ychange = a * a * (1 - 2 * b)
        ellipseError = 0
        stoppingX = 0
        stoppingY = twoASquare * b

        while stoppingX <= stoppingY:
            plot_ellipse_4_points(x0, y0, x, y)
            x += 1
            stoppingX += twoBSquare
            ellipseError += xchange
            xchange += twoBSquare

            if (2 * ellipseError + ychange) > 0:
                y -= 1
                stoppingY -= twoASquare
                ellipseError += ychange
                ychange += twoASquare
                
    def draw_hyperbola(self, x0, y0, a, b):
        step = 0.5 
        x = a 

        while x < a * 5:
            y_squared = (b**2) * ((x**2) / (a**2) - 1)
            
            if y_squared >= 0:  
                y = math.sqrt(y_squared)
                
                self.root.after(1, self.draw_point, x0 + x, y0 + y)
                self.root.after(1, self.draw_point, x0 + x, y0 - y)
                self.root.after(1, self.draw_point, x0 - x, y0 + y)
                self.root.after(1, self.draw_point, x0 - x, y0 - y)

            x += step 


    def draw_parabola(self, x0, y0, a):
        step = 0.5  
        x = 0 

        while x < abs(a) * 5: 
            y = (x ** 2) / (4 * abs(a))  

            if a > 0:  
                self.root.after(1, self.draw_point, x0 + x, y0 - y) 
                self.root.after(1, self.draw_point, x0 - x, y0 - y)  
            else:  
                self.root.after(1, self.draw_point, x0 + x, y0 + y) 
                self.root.after(1, self.draw_point, x0 - x, y0 + y) 

            x += step


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalEditor(root)
    root.mainloop()
