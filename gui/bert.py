import torch
import pandas as pd
import numpy as np
import sys
from transformers import BertModel, BertTokenizer
from os import path
from torch import nn
from torch.nn import functional as F
import os.path
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from test_data_generator import generate_test_data

PRE_TRAINED_MODEL_NAME= 'bert-base-cased'


class InterestClassifier(nn.Module):
    
  def __init__(self, n_classes):
    super(InterestClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask
    )
    output = self.drop(pooled_output)
    return self.out(output)



class Bert:

  def __init__(self,model_path,class_names):
      self.model_path=model_path
      self.class_names=class_names
      self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
      self.model = InterestClassifier(len(class_names))
      self.MAX_LEN = 175
      self.PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
      self.tokenizer = BertTokenizer.from_pretrained(self.PRE_TRAINED_MODEL_NAME)
      print("test")
      
  def get_prediction_array(self,review_text):
      encoded_review =self.tokenizer.encode_plus(
        review_text,
        max_length=self.MAX_LEN,
        add_special_tokens=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
      )
  
      input_ids = encoded_review['input_ids'].to(self.device)
      attention_mask = encoded_review['attention_mask'].to(self.device)
      
      output =self.model(input_ids, attention_mask)
      return output
  
    
  def get_interests(self,test_df, threshold):
      predictions=[0] * len(self.class_names)
      for index in tqdm(range(min(threshold, len(test_df)))):
        caption = test_df["captions"][index]
        prediction=F.softmax(self.get_prediction_array(caption), dim = 1)
        prediction=prediction[:].detach().cpu().numpy()
        predictions=predictions+prediction
      data_len=len(test_df["captions"])
      if data_len>0 :
        predictions=(1/data_len)*predictions
    
      return predictions
  
  def load_model(self):
      state_dict = torch.load(self.model_path, map_location=torch.device('cpu'))
      self.model.load_state_dict(state_dict)
      self.model.to(self.device)
      
      
      
  def predict(self,user_account,threshold, test_df):
    #test_df=generate_test_data(user_account,threshold)
    final_pred =self.get_interests(test_df,threshold)
    return final_pred

