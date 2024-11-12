import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from moviepy.editor import TextClip, concatenate_videoclips, ImageClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

def text_to_video(text, duration, output_file, bg_image_path=None):
    # Cria um arquivo de áudio a partir do texto
    tts = gTTS(text, lang='pt')
    tts.save("temp_audio.mp3")
    audio = AudioFileClip("temp_audio.mp3")

    # Cria uma imagem de fundo
    if bg_image_path:
        img = Image.open(bg_image_path).convert("RGB")
    else:
        img = Image.new('RGB', (1920, 1080), color=(73, 109, 137))
    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 70)
    w, h = draw.textsize(text, font=font)
    draw.text(((1920 - w) / 2, (1080 - h) / 2), text, fill="white", font=font)
    img.save('temp_image.png')

    # Cria um clipe de vídeo com a imagem
    clip = ImageClip('temp_image.png', duration=duration).set_audio(audio)

    # Salva o vídeo
    clip.write_videofile(output_file, fps=24)

    # Remove arquivos temporários
    os.remove("temp_audio.mp3")
    os.remove("temp_image.png")

# Função principal para obter texto e gerar o vídeo
def main():
    # Solicita a entrada do usuário
    user_input = input("Digite o texto para o vídeo: ")
    duration_str = input("Duração do vídeo em segundos: ")
    
    try:
        # Conversão da duração para inteiro
        duration = int(duration_str)
    except ValueError:
        print("Por favor, insira a duração em segundos como um número inteiro.")
        return

    output_file = input("Nome do arquivo de saída (ex: output_video.mp4): ")
    
    # Gerar vídeo
    text_to_video(user_input, duration, output_file)

if __name__ == "__main__":
    main()
