import numpy as np
import librosa
from PIL import Image
import imagehash
# from imagehash import hex_to_hash
from scipy import signal


def Load_Audio(file_name, file_data, sr):
    song_name = file_name
    song_data = file_data
    song_datatype = file_data.dtype
    song_dict = {
        "name": song_name,
        "data": song_data,
        "sr": sr,
        "dType": song_datatype,
        "spectrogram_Hash": None,
        "melspectrogram_Hash": None,
        "mfcc_Hash": None,
        "chroma_stft_Hash": None,
    }
    return song_dict


def Features(file_data, sr, spectro):
    #spectro
    melspectro = librosa.feature.melspectrogram(file_data, sr=sr, S=spectro)
    #chroma_stft
    chroma_stft = librosa.feature.chroma_stft(file_data, sr=sr, S=spectro)
    #spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound
    # spectral_centroids = librosa.feature.spectral_centroid(file, sr=sr)[0]
    mfccs = librosa.feature.mfcc(file_data.astype('float64'), sr=sr)

    return [melspectro, mfccs, chroma_stft]


def Hash(feature) -> str:
    data = Image.fromarray(feature)
    return imagehash.phash(data, hash_size = 16).__str__()


def Load_Song(file_name,file_data,sr) -> dict:
    #Loads audio file, create a spectrogram, extract some features and hash them.

    song = Load_Audio(file_name, file_data, sr)
    #colorMesh = sxx = spectrogram ndarray
    f, t, colorMesh = signal.spectrogram(song['data'], fs=song['sr'], window='hann')
    features = Features(song['data'], song['sr'], colorMesh)
    song['spectrogram_Hash'] = Hash(colorMesh)
    song['melspectrogram_Hash'] = Hash(features[0])
    song['mfcc_Hash'] = Hash(features[1])
    song['chroma_stft_Hash'] = Hash(features[2])
    return song
