from bert import Bert

class_names=['shopping and  fashion', 'food and drink', 'technology',
       'business and industry', 'entertainment',
       'family and relationships', 'fitness and wellness',
       'hobbies and activities', 'sports and outdoors']

class_names = ['shopping and  fashion', 'entertainment', 'food and drink', 'hobbies and activities', 'technology', 'business and industry', 'family and relationships', 'fitness and wellness', 'sports and outdoors']
#class_names = ['food and drink', 'entertainment', 'technology', 'shopping and  fashion', 'family and relationships', 'hobbies and activities', 'fitness and wellness', 'sports and outdoors', 'business and industry']
model_path="C:/Users/Test/Documents/GitHub/test_wassim_CNN/model_all_captions_hashtags_12k.h5" #hott elpath mta3 elbert model

class BertTester():
    
    def test_bert(self,user_account,threshold, test_df, bert):
        if (not bert):
            bert=Bert(model_path,class_names)
            bert.load_model()
        prediction = bert.predict(user_account,threshold, test_df)
        return prediction
        
        
if __name__=="__main__":
    user_account="skyemcalpine"
    threshold=30       
    bertTester=BertTester()
    prediction=bertTester.test_bert(user_account,threshold, test_df)
    print(prediction)
    print(class_names)