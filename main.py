import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # PIL for handling images

# Game content
game_text = {
    "start": {
        "text": "You awaken in a dark dungeon. Two paths lie before you.",
        "choices": [("Take the left path", "left_path"), ("Take the right path", "right_path")]
    },
    "left_path": {
        "text": "You walk into the darkness. A glowing orb floats toward you.",
        "choices": [("Touch the orb", "orb_touch"), ("Avoid it", "orb_avoid")]
    },
    "right_path": {
        "text": "You find a fire-breathing lizard!",
        "choices": [("Fight the lizard", "fight_lizard"), ("Run back", "start")]
    },
    "orb_touch": {
        "text": "The orb explodes! You die from the gas. 💀",
        "choices": [("Try again", "start")]
    },
    "orb_avoid": {
        "text": "You avoid the orb and find a ladder going up...",
        "choices": [("Climb the ladder", "escape")]
    },
    "fight_lizard": {
        "text": "The lizard roasts you. 💀",
        "choices": [("Try again", "start")]
    },
    "escape": {
        "text": "You climb out and see the sunlight. You’ve escaped! 🏆",
        "choices": [("Play again", "start")]
    }
}

class DungeonGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escape the Dungeon")
        self.geometry("700x450")
        self.resizable(False, False)

        # Load background image
        self.bg_image = Image.open("etd.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create background label
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Overlay frame for story and buttons
        self.overlay = tk.Frame(self, bg="#00000080")  # semi-transparent background
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

        self.story_label = tk.Label(self.overlay, text="", wraplength=600, justify="left",
                                    font=("Georgia", 14), fg="white", bg="#00000080")
        self.story_label.pack(pady=10)

        self.button_frame = tk.Frame(self.overlay, bg="#00000000")
        self.button_frame.pack()

        self.display_scene("start")

    def display_scene(self, scene_key):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        scene = game_text[scene_key]
        self.story_label.config(text=scene["text"])

        for choice_text, next_scene in scene["choices"]:
            btn = tk.Button(self.button_frame, text=choice_text,
                            command=lambda s=next_scene: self.display_scene(s),
                            font=("Helvetica", 12), bg="#222", fg="white",
                            activebackground="#555", width=30)
            btn.pack(pady=4)

if __name__ == "__main__":
    app = DungeonGame()
    app.mainloop()
