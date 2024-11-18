import jiwer

import pandas as pd

gt_stutter = 'librispeech_result\gt_librispeech.csv'
stutter_transcription = 'data.csv'

df_gt_stutter = pd.read_csv(gt_stutter)
df_stutter_transcription = pd.read_csv(stutter_transcription)

print(df_gt_stutter.shape)
print(df_stutter_transcription.shape)
# Merging dataframes based on the filename column
df_gt_stutter_clean = df_gt_stutter.drop(df_gt_stutter.columns[0], axis=1)

# Reset the index if needed
df_gt_stutter_clean = df_gt_stutter_clean.reset_index(drop=True)
#df_gt_stutter_clean = df_gt_stutter_clean.drop('total_stutter', axis=1)
df_gt_stutter_clean['file_name'] = df_gt_stutter_clean['file_name'].str.replace('.csv', '', regex=False)

# Remove the first column (index 0)
df_stutter_transcription_clean = df_stutter_transcription.drop(df_stutter_transcription.columns[0], axis=1)

# Reset the index if needed
df_stutter_transcription_clean['file_name'] = df_stutter_transcription_clean['file_name'].str.replace('.flac', '', regex=False)

merged_df = pd.merge(df_gt_stutter_clean[['file_name', 'ground_truth']], df_stutter_transcription_clean[['Filename', 'TunedTranscription']], on='file_name')

# Display the merged dataframe
print(merged_df.head)

# Calculate WER for each pair of ground truth and prediction
ground_truth_list = merged_df['ground_truth'].tolist()
prediction_list = merged_df['prediction'].tolist()

# Calculate WER for each row
wer_results = [
    jiwer.wer(gt, pred)
    for gt, pred in zip(ground_truth_list, prediction_list)
]

# Add WER results to the dataframe
merged_df['wer'] = wer_results

# Calculate the mean WER
mean_wer = merged_df['wer'].mean()

print(f"The mean Word Error Rate is: {mean_wer:.4f}")