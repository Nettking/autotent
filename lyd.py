from gtts import gTTS
import os

def lag_lydfil(tekst, språk='en'):
    # Opprett et gTTS-objekt med den angitte teksten og språket
    tts = gTTS(text=tekst, lang=språk, slow=False)

    # Lagre lydfilen som en MP3-fil
    lydfil_navn = 'output.mp3'
    tts.save(lydfil_navn)

    print(f'Lydfilen "{lydfil_navn}" er opprettet.')

    # Åpne den opprettede lydfilen med standard lydavspiller
    os.system(f'start {lydfil_navn}')  # Dette fungerer på Windows, for andre systemer må du justere kommandoen

if __name__ == "__main__":
    # Spesifiser banen til tekstfilen
    tekstfil_bane = 'tekstfil.txt'

    try:
        # Les innholdet fra tekstfilen
        with open(tekstfil_bane, 'r', encoding='utf-8') as fil:
            tekst_innhold = fil.read()

        # Lag lydfil basert på innholdet i tekstfilen
        lag_lydfil(tekst_innhold)

    except FileNotFoundError:
        print(f'Filen "{tekstfil_bane}" ble ikke funnet.')
    except Exception as e:
        print(f'En feil oppstod: {e}')
