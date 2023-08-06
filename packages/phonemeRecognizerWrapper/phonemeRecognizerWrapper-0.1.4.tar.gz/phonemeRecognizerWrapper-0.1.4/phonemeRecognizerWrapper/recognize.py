# ----------------------------------------------------------------------------------------------------------------------
# recognize.py
# This script uses the Allosaurus phoneme recognition package to extract phonemic content from audio files of human
# speech. This script acts as a wrapper over the Allosaurus package for improved formatting and piping of data to
# MATLAB scripts for analysis (e.g. vowel formant extraction).
# ----------------------------------------------------------------------------------------------------------------------
# Command structure:
# <py -m phonemeRecognizerWrapper.recognize LANGUAGE_CODE FILES EMIT_PROB>
# ----------------------------------------------------------------------------------------------------------------------
# Required Arguments:
# 1) LANGUAGE_CODE: Three characters long language code supported by the Allosaurus library. For the list of available
#                   languages, use command <py -m allosaurus.bin.list_lang>. To display the phonetic inventory (list of
#                   phonemes) for a specific language, use <py -m allosaurus.bin.list_phone [--lang <language name>]>
#                   See https://github.com/xinjli/allosaurus for more info.
#                   * Example options:
#                   "ipa" - uses the whole available phonetic inventory for recognition (less accurate)
#                   "deu" - german
#                   "gsw" - swiss german
#                   "fra" - french
#                   "eng" - english
# 2) FILES: Absolute path to a temp .txt file containing a semicolon delimited string of absolute paths to all files
#           meant for recognition. Surround the string with apostrophes ("") if any of the paths contains spaces.
#           * Temp file contents example:
#           "C:\sounds\sound1.wav;C:\sounds\sound2.wav"

# Optional Arguments:
# 3) EMIT_PROB: Allosaurus setting that determines the phoneme emission rate of the underlying model. Higher number
#               tells the model to produce more phonemes, smaller number vice versa. Center is at 1.0, and optimal range
#               that produces comprehensive outputs is 0.8 - 1.5. If omitted, default value of 1.5 is used.
# ----------------------------------------------------------------------------------------------------------------------
# Example usage from command line:
# <py -m phonemeRecognizerWrapper.recognize eng "C:\sounds\sound.wav;C:\sounds\sound2.wav" 1.0>

# Example usage from MATLAB via the <[status, result] = system(command)> function:
# <command = 'py -m phonemeRecognizerWrapper.recognize" eng "C:\sounds\sound.wav;C:\sounds\sound2.wav" 1.0';>
# It is also recommended to use <set PYTHONIOENCODING=utf8> before the python command to ensure proper text formantting
# via the standard output pipe.
# ----------------------------------------------------------------------------------------------------------------------
# Developed at CTU Prague, FEE, October 2021
# Author: Vojtěch Illner
# Revision: June 2022, Petr Krýže
# ----------------------------------------------------------------------------------------------------------------------

# Imports
import os
import sys
from pathlib import Path

import pydub
from allosaurus.app import read_recognizer
from pydub import effects

########################################################################################################################
# Constants
DEFAULT_EMIT_PROBABILITY = 1.5  # Phoneme emit probability =~ how many phonemes will be generated
NORMALIZE_HEADROOM = 0.5  # Value in dB, separation of max signal peak and ceiling after normalization


# Load the Allosaurus language model with the specified setting.
def load_model(model_string):
    return read_recognizer(model_string)


def allosaurus_phon_rec(files, lang_phon, emit_phon):
    # Load the language model
    if lang_phon != 'eng':
        model_type = 'uni2005'
    else:
        model_type = 'eng2102'
    model = load_model(model_type)

    print("#ALLOSAURUS: Starting phoneme recognition of %d file(s)" % len(files))

    # Iterate over the files
    for file in files:
        print("#FILEPATH=%s" % file)
        print("#BEGIN")
        # Phoneme recognition step
        out = model.recognize(filename=file, lang_id=lang_phon, topk=2, emit=emit_phon, timestamp=True)

        # Prints the phoneme recognition output straight into the standard output for piping
        print(str(out))
        print("#END")

    print('#Process completed')


########################################################################################################################

# Run the script.
if __name__ == '__main__':
    # Retrieve input arguments
    try:
        # Required arguments
        input_lang = sys.argv[1]
        input_files_file_path = sys.argv[2]
        # Optional argument
        if len(sys.argv) <= 3:
            input_emit = DEFAULT_EMIT_PROBABILITY  # Get default emit probability
        else:
            input_emit = float(sys.argv[3])
    except IndexError:
        print('Invalid input arguments\n' +
              '1 - language code\n' +
              '2 - path to a temp text file containing a string with semicolon delimited input sound files for '
              'analysis\n' +
              '3 - float number indicating probability of emitting phonemes\n')
        sys.exit(-1)

    # Input files' paths are stored in a temp text file on the provided path (input_files_file_path), we need to
    # retrieve that file and get its content (just one long line)
    temp_file_path = Path(input_files_file_path)
    if not Path.is_file(temp_file_path):  # Check for file existence
        sys.stderr.write("Temp input file %s does not exist or is not a file!" % temp_file_path)
        sys.exit(-1)

    ext = temp_file_path.suffix.lower()
    if ext != ".txt":
        sys.stderr.write("Temp input file %s is not a TXT text file!" % temp_file_path)
        sys.exit(-1)

    input_files = Path.read_text(temp_file_path)

    # Input conditioning - parse input and check file existence
    processed_files = []
    if len(str(input_files)) > 0:
        input_files = (str(input_files)).split(";")
        for f in input_files:
            filepath = Path(f)
            if not Path.is_file(filepath):  # Check if the file exists
                sys.stderr.write("File %s does not exist or is not a file!" % f)
                sys.exit(-1)

            ext = filepath.suffix.lower()
            if ext != ".wav":  # Check if the file is a WAV
                sys.stderr.write("File %s is not a WAV audio file!" % f)
                sys.exit(-1)

            fol_path = filepath.parent  # Folder where the file is located
            temppath = fol_path.joinpath("temp")
            if not temppath.exists():  # Create the temp folder if it doesn't exist
                temppath.mkdir()

            out_filepath = temppath.joinpath("%s_PROCESSED.wav" % filepath.stem)
            if out_filepath.exists() and out_filepath.is_file():  # If the processed file exists, delete it
                os.remove(out_filepath)  # Deletes the file

            # Load the audio, normalized the volume and export as 16bit PCM WAV using pydub (retain sample rate)
            audio = pydub.AudioSegment.from_wav(filepath)
            normalized = effects.normalize(audio, headroom=NORMALIZE_HEADROOM)

            params = ["-ac", "1", "-ar", "%d" % audio.frame_rate]
            normalized.export(out_f=out_filepath, format='wav', codec="pcm_s16le", parameters=params)

            processed_files.append(out_filepath)  # Append the processed file list
            del audio  # Delete the object in memory, so it's not used and the temp file can be later deleted

    # Perform allosaurus phoneme recognition on all the specified files
    allosaurus_phon_rec(processed_files, input_lang, input_emit)

    # Delete all the processed files and the temp folder
    for f in processed_files:
        filepath = Path(f)
        if filepath.exists():
            filepath.unlink()

        if filepath.parent.exists() and filepath.parent.is_dir():
            if not os.listdir(filepath.parent):  # Directory is empty
                filepath.parent.rmdir()  # Delete the directory

    sys.exit(1)
