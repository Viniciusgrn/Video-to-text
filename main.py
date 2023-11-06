#Instalar FFMPEG manualmente
#https://www.hashtagtreinamentos.com/como-transcrever-audio-com-python

#Importando bibliotecas utilizadas
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm
import os

#Definindo as variaveis utilizadas
arquivo = 'joguinho'
mp4 = f'{arquivo}.mp4'
mp3 = f'{arquivo}.mp3'
wav = f'{arquivo}.wav'
txt = f'{arquivo}.txt'

#Tranforma o video MP4 em um áudio MP3


clip = mp.VideoFileClip(mp4).subclip()
clip.audio.write_audiofile(mp3)
print("PASSOU 1")
#O arquivo será convertido de MPE em WAV através da função AudioSegment
#Iremos então o ler utilizando o método export
#e salvaremos o áudio na váriavel WAV


sound = AudioSegment.from_mp3(mp3)
sound.export(wav, format='wav')
audio = AudioSegment.from_file(wav, 'wav')
print("PASSOU 2")
try:
    os.remove(mp3)
except:
    print("Arquivo inexistente")
print("PASSOU 3")
#Para que o texto seja extraido, é necessario que sejam criados vários arquivos de áudio
#Utilizaremos então a biblioteca pydub com sua função make_chunks, ela é responsavel por dividir o arquivo de áudio em tamanhos iguas

tamanho = 30000
partes = make_chunks(audio, tamanho)
partes_audio = []
for i, parte in tqdm(enumerate(partes)):
    parte_name = 'audio{0}.wav'.format(i)
    partes_audio.append(parte_name)
    parte.export(parte_name, format='wav')
print("PASSOU 4")
#Temos agora o arquivo wav em partes

# função que remove arquivo do S.O.
try:
    os.remove(wav)
except:
    print("Arquivo inexistente")
print("PASSOU 5")

def trascricao(nome_audio):
    r = sr.Recognizer()
    with sr.AudioFile(nome_audio) as source:
        audio = r.record(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR') #en-US
        print('Texto:' + texto)
    except sr.UnknownValueError:
        texto = ''
        print('Áudio não entendido')
    except sr.RequestError as e:
        texto = ''
        print('Erro ao solicitar resultados; {0}'.format(e))
    finally:
        try:
            os.remove(nome_audio)
        except:
            print('Arquivo inexistente')
    return texto
print("PASSOU 6")

texto = ''
for parte in tqdm(partes_audio):
    texto = texto + '' + trascricao(parte)
print("PASSOU 7")

#Gera txt
arquivoTxt = open(txt, 'w')
arquivoTxt.write(texto)
arquivo.close()
