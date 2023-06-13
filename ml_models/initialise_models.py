
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch


tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment", torchscript=True)
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment", torchscript=True)

torch.save(model,'model_sentiment_analyse.pt')
torch.save(tokenizer, 'tokenizer_sentiment_analyse.pt')



