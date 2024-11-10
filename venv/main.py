import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

def create_image_with_text(text, image_path, output_image_path, font_path):
    # Abre a imagem
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Carrega a fonte
    font = ImageFont.truetype(font_path, size=40)

    # Calcula a posição do texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # largura
    text_height = bbox[3] - bbox[1]  # altura
    position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

    # Desenha o texto na imagem
    draw.text(position, text, font=font, fill="white")

    # Salva a imagem com o texto
    image.save(output_image_path)

def generate_video(images, text, audio_path, font_path, resolution):
    output_images = []
    
    for i, image in enumerate(images):
        output_image_path = f"output_image_{i}.png"
        create_image_with_text(text, image, output_image_path, font_path)
        output_images.append(output_image_path)

    # Cria um vídeo a partir das imagens
    clip = ImageSequenceClip(output_images, fps=24)
    clip = clip.set_duration(5)  # Duração de 5 segundos para o vídeo
    clip.write_videofile("output_video.mp4", audio=audio_path)

def generate_video_wrapper(images, text, audio_path, font_path, resolution):
    generate_video(images, text, audio_path, font_path, resolution)

# Exemplo de uso
if __name__ == "__main__":
    # Defina os caminhos para as imagens, texto, áudio e fonte
    images = ["image1.jpg", "image2.jpg", "image3.jpg"]  # Substitua pelos caminhos reais das suas imagens
    text = "Seu Texto Aqui"  # Texto que será adicionado às imagens
    audio_path = "audio.mp3"  # Substitua pelo caminho real do seu áudio
    font_path = "arial.ttf"  # Substitua pelo caminho real da sua fonte
    resolution = (1280, 720)  # Resolução do vídeo

    generate_video_wrapper(images, text, audio_path, font_path, resolution)