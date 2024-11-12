import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\convert.exe"

from moviepy.editor import TextClip, concatenate_videoclips, ImageClip, AudioFileClip
from gtts import gTTS
from PIL import Image

def text_to_video(text, duration, output_file):
    # Cria um arquivo de áudio a partir do texto
    tts = gTTS(text, lang='pt')
    tts.save("temp_audio.mp3")
    audio = AudioFileClip("temp_audio.mp3")

    # Cria uma imagem com o texto
    img = Image.new('RGB', (1920, 1080), color=(73, 109, 137))
    img.save('temp_image.png')

    # Cria um clipe de vídeo com a imagem
    clip = ImageClip('temp_image.png', duration=duration)
    text_clip = TextClip(text, fontsize=70, color='white', size=(1920, 1080))
    text_clip = text_clip.set_duration(duration).set_position('center')

    video = concatenate_videoclips([clip.set_audio(audio)])

    # Adiciona o clipe de texto sobre a imagem
    final_video = concatenate_videoclips([video, text_clip.set_start(0).set_duration(duration)])

    # Salva o vídeo
    final_video.write_videofile(output_file, fps=24)

    # Remove arquivos temporários
    os.remove("temp_audio.mp3")
    os.remove("temp_image.png")

# Exemplo de uso
text = "Bem-vindo ao meu vídeo!"
duration = 10  # duração do vídeo em segundos
output_file = "output_video.mp4"
text_to_video(text, duration, output_file)
