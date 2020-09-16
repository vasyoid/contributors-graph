from tkinter import Tk, Canvas, Frame, BOTH, S, SW
from time import time

VERTEX_R = 6
FRAME_SIZE = 1000
zoom_factor = 80
x_offset = FRAME_SIZE / 2
y_offset = FRAME_SIZE / 2
threshold = 0


class GraphFrame(Frame):
    def __init__(self, graph):
        super().__init__()
        self.master.title('Graph')
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.graph = graph
        self.focus_set()
        self.bind('<Key>', on_key_event)
        self.bind('')
        self.canvas.pack(fill=BOTH, expand=1)


def zoom(event):
    global zoom_factor
    if event.detail == '<Button-4>':
        zoom_factor -= 10
    elif event.detail == '<Button-5>':
        zoom_factor += 10


def on_key_event(event):
    global x_offset, y_offset, zoom_factor, threshold
    if event.char == 'w':
        y_offset += 5
    elif event.char == 's':
        y_offset -= 5
    if event.char == 'a':
        x_offset += 5
    elif event.char == 'd':
        x_offset -= 5
    elif event.char == 'q':
        zoom_factor = max(10, zoom_factor - 10)
    elif event.char == 'e':
        zoom_factor = min(1000, zoom_factor + 10)
    elif event.char == 'z':
        threshold = max(0, threshold - 0.01)
    elif event.char == 'c':
        threshold = min(0.99, threshold + 0.01)


def to_screen(a):
    return (a[0] - 0.5) * zoom_factor + x_offset, (a[1] - 0.5) * zoom_factor + y_offset


def draw_graph(frame, pt):

    ct = time()
    dt = ct - pt

    for i in range(40):
        frame.graph.update(dt, threshold)

    frame.canvas.delete('all')

    for (u, v), weight in frame.graph.edges.items():
        if weight > threshold:
            u = to_screen(frame.graph.vertices[u])
            v = to_screen(frame.graph.vertices[v])
            frame.canvas.create_line(u[0], u[1], v[0], v[1], fill='#999999')

    for k, v in frame.graph.vertices.items():
        v = to_screen(v)
        frame.canvas.create_oval(v[0] - VERTEX_R, v[1] - VERTEX_R, v[0] + VERTEX_R, v[1] + VERTEX_R, fill='#aaffaa')
        frame.canvas.create_text(v[0], v[1] - VERTEX_R, text=k, anchor=S)

    frame.canvas.create_text(0, FRAME_SIZE, text=f'connection threshold: {threshold:.2f}', anchor=SW, font='Noto 20')
    frame.after(40, draw_graph, frame, ct)


def run_frame(graph):
    root = Tk()
    frame = GraphFrame(graph)
    root.geometry(f'{FRAME_SIZE}x{FRAME_SIZE}')
    draw_graph(frame, time())
    root.mainloop()
