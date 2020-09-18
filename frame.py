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


def init_canvas(frame):
    for k, weight in frame.graph.edges.items():
        if weight > 0:
            frame.graph.edges_ids[k] = frame.canvas.create_line(-1, -1, -1, -1, fill='#999999')

    for k, v in frame.graph.vertices.items():
        frame.graph.vertices_ids[k] = frame.canvas.create_oval(0, 0, 0, 0, fill='#aaffaa')
        frame.graph.labels_ids[k] = frame.canvas.create_text(0, 0, text=k, anchor=S)

    text_id = frame.canvas.create_text(0, FRAME_SIZE, text=f'connection threshold: {threshold:.2f}', anchor=SW, font='Noto 20')
    draw_graph(frame, time(), text_id)


def draw_graph(frame, pt, text_id):

    ct = time()
    dt = ct - pt

    frame.graph.update(dt, threshold)

    for (u, v), weight in frame.graph.edges.items():
        if weight > threshold:
            pu = to_screen(frame.graph.vertices[u])
            pv = to_screen(frame.graph.vertices[v])
            frame.canvas.coords(frame.graph.edges_ids[u, v], pu[0], pu[1], pv[0], pv[1])
        elif (u, v) in frame.graph.edges_ids:
            frame.canvas.coords(frame.graph.edges_ids[u, v], -1, -1, -1, -1)

    for k, v in frame.graph.vertices.items():
        pv = to_screen(v)
        frame.canvas.coords(frame.graph.vertices_ids[k], pv[0] - VERTEX_R, pv[1] - VERTEX_R, pv[0] + VERTEX_R, pv[1] + VERTEX_R)
        frame.canvas.coords(frame.graph.labels_ids[k], pv[0], pv[1] - VERTEX_R)

    frame.canvas.itemconfig(text_id, text=f'connection threshold: {threshold:.2f}')
    frame.after(100, draw_graph, frame, ct, text_id)


def run_frame(graph):
    root = Tk()
    frame = GraphFrame(graph)
    root.geometry(f'{FRAME_SIZE}x{FRAME_SIZE}')
    init_canvas(frame)
    root.mainloop()
