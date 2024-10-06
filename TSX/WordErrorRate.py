import pandas as pd
from jiwer import wer


gt= "librispeech_result\gt_librispeech.csv"
wav_trans = "librispeech_result\wav2vec_librispeech.csv"


# Read the CSV file into a DataFrame

# Ground Truth
df_gt = pd.read_csv(gt)
df_gt = df_gt.drop('Unnamed: 0', axis=1)
df_gt.rename(columns={'ground_truth': 'text'}, inplace=True)

# AI Transcription
df_wav_trans = pd.read_csv(wav_trans)
df_wav_trans = df_wav_trans.drop('Unnamed: 0', axis=1)
df_wav_trans['file_name'] = df_wav_trans['file_name'].str.replace('.flac', '', regex=False)
df_wav_trans.rename(columns={'prediction': 'text'}, inplace=True)


# Print the DataFrame
#print(df_gt)
#print(df_wav_trans)


dict_gt = df_gt.set_index('file_name')['text'].to_dict()
dict_wav_trans = df_wav_trans.set_index('file_name')['text'].to_dict()

# Prints both dictionaries
#print(dict_gt)
#print(dict_wav_trans)

error = 0
for k in dict_wav_trans.keys(): # DOES NOT GO THROUGH ALL OF GROUND TRUTH BEACUSE wav_trans csv does not have all the transcriptions that ground truth does
  error += wer(dict_wav_trans[k], dict_gt[k])

print(error)
print(error/len(df_wav_trans))



print(wer("my name is a john","my name is a ajohn")) # It sees that there is one mistake and 5 words, therefore it puts 1/5 = .2 as the error
print(wer(" hi my name is john","my name is john")) # Even if it doesn't catch one word in the start, it doesn't mess with the rest of the sentence




