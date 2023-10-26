from datasets import load_dataset
import spacy
dataset = load_dataset('patriziobellan/PET')

for sentence in dataset['test']:
    print(sentence)