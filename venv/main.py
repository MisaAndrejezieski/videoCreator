import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, messagebox
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

def create_image_with_text(text, image_path, output_image_path, font_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=40)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

    draw.text(position, text, font=font, fill="white")
    image.save(output_image_path)

def generate_video(images, text, audio_path, font_path):
    output_images = []
    
    for i, image in enumerate(images):
        output_image_path = f"output_image_{i}.png"
        create_image_with_text(text, image, output_image_path, font_path)
        output_images.append(output_image_path)

    clip = ImageSequenceClip(output_images, fps=24)
    clip = clip.set_duration(5)
    clip.write_videofile("output_video.mp4", audio=audio_path)

def select_images():
    files = filedialog.askopenfilenames(title="Selecione as Imagens", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if files:
        images_var.set(';'.join(files))

def select_audio():
    file = filedialog.askopenfilename(title="Selecione o Áudio", filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file:
        audio_var.set(file)

def select_font():
    file = filedialog.askopenfilename(title="Selecione a Fonte", filetypes=[("Font Files", "*.ttf")])
    if file:
        font_var.set(file)

def generate_video_wrapper():
    images = images_var.get().split(';')
    text = text_var.get()
    audio_path = audio_var.get()
    font_path = font_var.get()

    if not images or not text or not audio_path or not font_path:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        generate_video(images, text, audio_path, font_path)
        messagebox.showinfo("Sucesso", "Vídeo gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Configuração da interface gráfica
root = Tk()
root.title("Criador de Vídeo")

images_var = StringVar()
audio_var = StringVar()
font_var = StringVar()
text_var = StringVar()

Label(root, text="Texto:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=text_var).grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Imagens:").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=images_var).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Selecionar Imagens", command=select_images).grid(row=1, column=2, padx=10, pady=10)

Label(root, text="Áudio:").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=audio_var).grid(row=2, column=1, padx=10, pady=10)
Button(root, text="Selecionar Áudio", command=select_audio).grid(row=2, column=2, padx=10, pady=10)

Label(root, text="Fonte:").grid(row=3, column=0, padx=10, pady=10)
Entry(root, textvariable=font_var).grid(row=3, column=1, padx=10, pady=10)
Button(root, text="Selecionar Fonte", command=select_font).grid(row=3, column=2, padx=10, pady=10)

Button(root, text="Gerar Vídeo", command=generate_video_wrapper).grid(row=4, column=1 , padx=10, pady=20)

root.mainloop()
