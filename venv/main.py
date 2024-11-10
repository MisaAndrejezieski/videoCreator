import os
from tkinter import *
from tkinter import filedialog, messagebox
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

def create_image_with_text(text, image_path, output_path, font_path=None):
    """Cria uma nova imagem com o texto sobreposto."""
    image = Image.open(image_path).convert("RGBA")
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    font = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
    text_width, text_height = d.textsize(text, font=font)
    text_x = (image.width - text_width) // 2
    text_y = image.height - text_height - 10
    d.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    combined = Image.alpha_composite(image.convert("RGBA"), txt)
    combined.save(output_path)

def generate_video(images, text, audio_path, font_path, resolution):
    """Gera um vídeo a partir de uma lista de imagens, texto e áudio."""
    clips = []
    
    for image in images:
        output_image_path = "temp_image.png"
        create_image_with_text(text, image, output_image_path, font_path)
        
        # Criando um clipe de vídeo a partir da imagem
        clip = ImageClip(output_image_path).set_duration(3)  # Duração de 3 segundos
        
        # Adicionando efeito de desvanecimento
        clip = clip.crossfadein(1)  # Transição de 1 segundo
        clips.append(clip)

    # Concatenando todos os clipes
    video = concatenate_videoclips(clips, method="compose")
    
    # Adicionando áudio se fornecido
    if audio_path:
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)

    # Redimensionando o vídeo se a resolução não for padrão
    if resolution != "Padrão":
        width, height = map(int, resolution.split('x'))
        video = video.resize(newsize=(width, height))

    # Exportando o vídeo
    video.write_videofile("output_video.mp4", fps=24)
    os.remove("temp_image.png")
    messagebox.showinfo("Sucesso", "Vídeo gerado com sucesso!")

def select_images():
    """Permite ao usuário selecionar múltiplas imagens."""
    files = filedialog.askopenfilenames(title="Selecionar Imagens", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    for file in files:
        images_listbox.insert(END, file)

def select_audio():
    """Permite ao usuário selecionar um arquivo de áudio."""
    file = filedialog.askopenfilename(title="Selecionar Áudio", filetypes=[("Audio Files", "*.mp3;*.wav")])
    audio_entry.delete(0, END)
    audio_entry.insert(0, file)

def select_font():
    """Permite ao usuário selecionar um arquivo de fonte."""
    file = filedialog.askopenfilename(title="Selecionar Fonte", filetypes=[("Font Files", "*.ttf")])
    font_entry.delete(0, END)
    font_entry.insert(0, file)

def generate_video_wrapper():
    """Coleta as entradas do usuário e gera o vídeo."""
    images = list(images_listbox.get(0, END))
    text = text_entry.get()
    audio_path = audio_entry.get()
    font_path = font_entry.get()
    resolution = resolution_var.get()
    
    if not images or not text:
        messagebox.showwarning("Aviso", "Por favor, insira texto e selecione imagens.")
        return
    
    generate_video(images, text, audio_path, font_path, resolution)

# Configurando a interface gráfica
root = Tk()
root.title("Gerador de Vídeo")
root.geometry("400x500")

# Texto
Label(root, text="Texto:").pack(pady=5)
text_entry = Entry(root, width= 50)
text_entry.pack(pady=5)

# Seleção de imagens
Label(root, text="Imagens:").pack(pady=5)
images_listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=10)
images_listbox.pack(pady=5)
Button(root, text="Selecionar Imagens", command=select_images).pack(pady=5)

# Seleção de áudio
Label(root, text="Áudio (opcional):").pack(pady=5)
audio_entry = Entry(root, width=50)
audio_entry.pack(pady=5)
Button(root, text="Selecionar Áudio", command=select_audio).pack(pady=5)

# Seleção de fonte
Label(root, text="Fonte (opcional):").pack(pady=5)
font_entry = Entry(root, width=50)
font_entry.pack(pady=5)
Button(root, text="Selecionar Fonte", command=select_font).pack(pady=5)

# Resolução
Label(root, text="Resolução:").pack(pady=5)
resolution_var = StringVar(value="Padrão")
Radiobutton(root, text="Padrão", variable=resolution_var, value="Padrão").pack(anchor=W)
Radiobutton(root, text="1280x720", variable=resolution_var, value="1280x720").pack(anchor=W)
Radiobutton(root, text="1920x1080", variable=resolution_var, value="1920x1080").pack(anchor=W)

# Botão para gerar vídeo
Button(root, text="Gerar Vídeo", command=generate_video_wrapper).pack(pady=20)

root.mainloop()
