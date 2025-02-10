import tkinter as tk
import time

class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический Редактор")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.current_algorithm = None

        self.draw_bresenham_button = tk.Button(self.button_frame, text="Алгоритм Брезенхэма", command=self.set_bresenham)
        self.draw_bresenham_button.pack(side=tk.LEFT, padx=5)

        self.draw_cda_button = tk.Button(self.button_frame, text="Алгоритм ЦДА", command=self.set_cda)
        self.draw_cda_button.pack(side=tk.LEFT, padx=5)

        self.draw_wu_button = tk.Button(self.button_frame, text="Алгоритм Ву", command=self.set_wu)
        self.draw_wu_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(self.button_frame, text="Назад", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.start_coords = None
        self.end_coords = None
        self.points = []
        self.canvas.bind("<Button-1>", self.add_point)

    def set_bresenham(self):
        self.current_algorithm = 'bresenham'
        print("Выбран алгоритм Брезенхэма")

    def set_cda(self):
        self.current_algorithm = 'cda'
        print("Выбран алгоритм ЦДА")

    def set_wu(self):
        self.current_algorithm = 'wu'
        print("Выбран алгоритм Ву")

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')
        print(f"Точка добавлена: ({x}, {y})")

        if len(self.points) == 1:
            self.start_coords = (x, y)
        elif len(self.points) == 2:
            self.end_coords = (x, y)
            self.draw_line()

    def draw_line(self):
        if self.start_coords and self.end_coords:
            if self.current_algorithm == 'bresenham':
                self.bresenham(self.start_coords, self.end_coords)
            elif self.current_algorithm == 'cda':
                self.cda_algorithm(self.start_coords, self.end_coords)
            elif self.current_algorithm == 'wu':
                self.wu_algorithm(self.start_coords, self.end_coords)

            self.points.clear()
            self.start_coords = None
            self.end_coords = None

    def bresenham(self, start, end):
        print(f"Расчет линии от {start} до {end}")
        
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        print(f"Начальные значения: dx={dx}, dy={dy}, sx={sx}, sy={sy}, err={err}")

        while True:
            self.canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, fill='blue') 
            self.canvas.update() 
            time.sleep(0.001) 

            print(f"Текущая точка: ({x1}, {y1}), err={err}")

            if x1 == x2 and y1 == y2:
                print("Достигнута конечная точка.")
                break

            err2 = err * 2
            
            if err2 > -dy:
                err -= dy
                x1 += sx
                print(f"Сдвиг по x: новый x1={x1}, err={err}")
            if err2 < dx:
                err += dx
                y1 += sy
                print(f"Сдвиг по y: новый y1={y1}, err={err}")

    def cda_algorithm(self, start, end):
        print(f"Расчет линии ЦДА от {start} до {end}")
        
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        print(f"dx={dx}, dy={dy}, steps={steps}")

        if steps == 0:
            self.canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, fill='blue')
            print("Линия состоит из одной точки.")
            return

        x_inc = dx / steps
        y_inc = dy / steps

        print(f"x_inc={x_inc}, y_inc={y_inc}")

        x, y = x1, y1
        for i in range(steps + 1):
            self.canvas.create_oval(int(round(x)) - 1, int(round(y)) - 1, int(round(x)) + 1, int(round(y)) + 1, fill='blue')
            self.canvas.update()
            time.sleep(0.001)  

            print(f"Шаг {i}: текущие координаты (x={x}, y={y})")

            x += x_inc
            y += y_inc

    def wu_algorithm(self, start, end):
        print(f"Расчет линии Ву от {start} до {end}")
        
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        print(f"Начальные значения: dx={dx}, dy={dy}")

        steps = max(abs(dx), abs(dy))
        print(f"Количество шагов (steps) = {steps}")

        if steps == 0:
            self.canvas.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, fill='blue')
            print("Линия состоит из одной точки.")
            return

        x_inc = dx / steps
        y_inc = dy / steps

        print(f"x_inc={x_inc}, y_inc={y_inc}")

        x, y = x1, y1

        for i in range(steps + 1):
            brightness = 1 - (i / steps)
            color = f'#{int(255 * brightness):02x}{int(255 * brightness):02x}{255:02x}' 
            
            self.canvas.create_oval(int(round(x)) - 1, int(round(y)) - 1, int(round(x)) + 1, int(round(y)) + 1, fill=color)
            self.canvas.update()
            time.sleep(0.001) 

            print(f"Шаг {i}: текущие координаты (x={x}, y={y}), цвет={color}")

            x += x_inc
            y += y_inc

    def clear_canvas(self):
        self.canvas.delete("all") 
        self.points.clear()
        self.start_coords = None
        self.end_coords = None
        print("Холст очищен")

    def go_back(self):
        self.root.destroy()

def open_lab():
    lab_window = tk.Tk()
    editor = GraphicEditor(lab_window)
    lab_window.mainloop()