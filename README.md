# Stuttered Speech ASR

A machine learning project by PInT (Public Interest in Tech) at Olin College of Engineering focused on improving automatic speech recognition (ASR) systems for people who stutter through fine-tuning state-of-the-art models and specialized preprocessing techniques.

## Overview

This project addresses the challenge of accurately recognizing speech from people who stutter (PWS). Traditional ASR systems often struggle with stuttered speech due to disfluencies such as repetitions, prolongations, and blocks.

Our goal is to improve accessibility by fine-tuning state-of-the-art ASR models (Whisper, Wav2Vec, etc.) on stuttered speech datasets, applying specialized preprocessing and evaluation tailored to this population.

## Problem Statement

Stuttering affects approximately 70 million people worldwide, yet most commercial ASR systems are not optimized for recognizing stuttered speech patterns. This creates accessibility barriers for people who stutter when interacting with voice-controlled technologies.

**Common stuttering disfluencies:**
- **Repetitions** – repeating sounds, syllables, or words
- **Prolongations** – stretching out sounds  
- **Blocks** – involuntary pauses or inability to produce sounds

## Features

- Specialized preprocessing for stuttered speech audio
- Model architectures adapted for disfluency patterns
- Data augmentation techniques for limited stuttered datasets
- Evaluation metrics tailored for stuttered speech recognition (e.g., WER analysis)
- Comparative analysis against standard ASR models
- Support for multiple languages (English and Mandarin)
- Fine-tuning implementations for Whisper and Wav2Vec models

## Repository Structure

```
.
├── FineTuneWhisper1.ipynb              # Initial Whisper fine-tuning
├── FineTune_Whisper_English.ipynb      # English Whisper fine-tuning
├── FineTune_Whisper_Mandarin.ipynb     # Mandarin Whisper fine-tuning
├── FineTune_Wav2Vec_English.ipynb      # English Wav2Vec fine-tuning
├── FineTune_Wav2Vec_Mandarin.ipynb     # Mandarin Wav2Vec fine-tuning
├── multi_lingual_speech_recognition.ipynb  # Multilingual ASR modeling
├── wer.ipynb                           # Word Error Rate analysis
├── SplitSet.ipynb                      # Dataset splitting utilities
├── processStutterGT.py                 # Data preprocessing script
├── requirements.txt                    # Python dependencies
├── train_data.csv                      # Training dataset
├── test_data.csv                       # Test dataset
├── examples/                           # Example audio files and usage
├── analysis/                           # Analysis results and visualizations
├── asr_processing/                     # ASR processing utilities
├── asr_processing_test/                # Testing utilities
├── libristutter_result/                # Results on LibriStutter dataset
├── librispeech_result/                 # Results on LibriSpeech dataset
├── StutterGTData/                      # StutterGT dataset files
├── wer_scores_csv/                     # WER evaluation results
└── [various merged/filtered CSV files] # Processed datasets
```

## Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook / JupyterLab
- CUDA-compatible GPU (recommended for training) (Google Colab was used for this project) 

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dongim04/stuttered-speech-asr.git
cd stuttered-speech-asr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Workflow

### 1. Data Preparation

Preprocess your stuttered speech dataset using the provided utilities:

```bash
# Using the preprocessing script
python processStutterGT.py

# Or using the Jupyter notebook
jupyter notebook SplitSet.ipynb
```

### 2. Fine-Tuning ASR Models

#### Whisper Models
- **General**: `FineTuneWhisper1.ipynb`
- **English**: `FineTune_Whisper_English.ipynb`
- **Mandarin**: `FineTune_Whisper_Mandarin.ipynb`

#### Wav2Vec Models
- **English**: `FineTune_Wav2Vec_English.ipynb`
- **Mandarin**: `FineTune_Wav2Vec_Mandarin.ipynb`

### 3. Multilingual Modeling

For cross-lingual experiments and multilingual model training:
```bash
jupyter notebook multi_lingual_speech_recognition.ipynb
```

### 4. Evaluation

Analyze model performance using Word Error Rate (WER) metrics:
```bash
jupyter notebook wer.ipynb
```

Results are automatically saved in:
- `wer_scores_csv/` - Detailed WER analysis
- `libristutter_result/` - Results on LibriStutter dataset
- `librispeech_result/` - Results on LibriSpeech dataset

## Example Usage

### Quick Start

1. **Preprocess your data:**
```bash
python processStutterGT.py
```

2. **Fine-tune a Whisper model for English:**
```bash
jupyter notebook FineTune_Whisper_English.ipynb
```

3. **Evaluate model performance:**
```bash
jupyter notebook wer.ipynb
```

### Working with Custom Data

The notebooks are designed to work with various stuttered speech datasets. Modify the data loading sections in the notebooks to work with your specific dataset format.

## Requirements

See `requirements.txt` for full dependencies. Key packages include:

- `torch` - PyTorch deep learning framework
- `transformers` - Hugging Face transformers library
- `jiwer` - Word Error Rate calculation
- `pandas`, `numpy` - Data manipulation
- `librosa`, `soundfile` - Audio processing
- `matplotlib`, `seaborn` - Visualization
- `datasets` - Hugging Face datasets library
- `accelerate` - Training acceleration

## Datasets

This project works with several stuttered speech datasets:

- **LibriStutter** - Stuttered version of LibriSpeech
- **StutterGT** - Ground truth stuttered speech dataset
- **LibriSpeech** - Used for comparison with fluent speech

*Note: Ensure you have proper permissions and follow ethical guidelines when working with speech data.*

## Results

The project includes comprehensive evaluation across multiple models and languages. Results are stored in:

- `wer_scores_csv/` - Detailed WER comparisons
- `analysis/` - Performance analysis and visualizations
- `*_result/` directories - Model-specific results

## Model Architectures

### Supported Models

1. **Whisper** (OpenAI)
   - Multilingual support
   - Various model sizes (tiny, base, small, medium, large)
   - Robust to background noise

2. **Wav2Vec 2.0** (Meta)
   - Self-supervised learning approach
   - Strong performance on limited data
   - Language-specific fine-tuning

## Contributing

Contributions, improvements, and feedback are welcome! 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution

- Additional model architectures
- New evaluation metrics
- Dataset preprocessing improvements
- Documentation enhancements
- Performance optimizations

## Ethical Considerations

This project is developed with respect for the stuttering community:

- Focuses on improving accessibility rather than "correcting" speech
- Maintains privacy and consent for all data usage
- Avoids perpetuating negative stereotypes about stuttering
- Emphasizes empowerment and inclusion

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{stuttered-speech-asr,
  author = {dongim04},
  title = {Stuttered Speech ASR: Fine-tuning ASR Models for People Who Stutter},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/dongim04/stuttered-speech-asr}
}
```

## Acknowledgments

- The stuttering research community for their valuable insights
- OpenAI for the Whisper model
- Meta for the Wav2Vec model
- Hugging Face for the transformers library
- Dataset creators and contributors

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

*This project aims to make voice technology more accessible for people who stutter while respecting the diversity and dignity of the stuttering community.*
