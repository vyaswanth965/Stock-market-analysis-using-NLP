import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import accuracy_score 
from sklearn.metrics import roc_auc_score 
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords

sw=set(stopwords.words('english'))
hold_words=['above' ,'below', 'down', "don't", "doesn't", "aren't" ,"didn't","are", 'not', 'no' ,'now', 'won'] 
for i in hold_words:
    sw.remove('{}'.format(i))
sw.add('.')
sw.add(':')  
sw.add(',') 
sw.add(';')
sw.add('&')
sw.add("'")
sw.add("it")
sw.add("'s")
sw.add("?")

data = pd.read_excel('TCSdata.xlsx')
print(data.head(10))

#print(data['loss/profit'])

# Removing punctuations
#data['news'].replace(to_replace="[^a-zA-Z]", value=" ", regex=True, inplace=True)
data['news'].replace('�',"'",inplace=True)
data['news']=data['news'].str.lower()


X = data["news"]
y = data["loss/profit"]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2, 
                                                    random_state=2000,
                                                    stratify=y)



basicvectorizer = CountVectorizer(ngram_range=(1,2),stop_words =frozenset(sw),analyzer='word')
basictrain = basicvectorizer.fit_transform(X_train)
print(basictrain.shape)


#basicmodel = RandomForestClassifier(n_estimators=300, criterion='entropy',max_features='auto')
basicmodel=XGBClassifier(max_depth=25, silent=False, n_estimators=200,objective="multi:softprob")
basicmodel = basicmodel.fit(basictrain, y_train)


basictest = basicvectorizer.transform(X_test)
y_pred = basicmodel.predict(basictest)

#pd.crosstab(y_test, y_pred, rownames=["Actual"], colnames=["Predicted"])


print(confusion_matrix(y_test, y_pred))
print (classification_report(y_test, y_pred))
print (accuracy_score(y_test, y_pred))
print(cohen_kappa_score(y_test, y_pred))
#print(roc_auc_score(y_test, y_pred))
#print(classification_report(y_test, y_pred))
#print(accuracy_score(y_test, y_pred))

