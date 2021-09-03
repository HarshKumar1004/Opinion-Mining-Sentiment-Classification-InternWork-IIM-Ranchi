#!/usr/bin/env python
# coding: utf-8

# # Opinion Mining + Sentiment Classification :
# ## For the Top 10 Indian Web Series(Comedy Genre)

# ### Getting The Data
# We have Web Scraped the user reviews from different OTT platforms(Amazon Prime,Netflix,ALT Balaji,ZEE5,Disney+Hotstar) for the top 10 Indian Web Series in Comedy Genre, on which our further analysis are done.

# In[1]:


import pandas as pd #for working with dataframes


# In[2]:


#Reading the webscraped reviews of all the the top 10 webseries of comedy genre.
r1_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",0)
r2_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",1)
r3_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",2)
r4_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",3)
r5_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",4)
r6_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",5)
r7_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",6)
r8_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",7)
r9_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",8)
r10_df=pd.read_excel(r"C:\Users\Asus\Desktop\Intern Work-IIM Ranchi\ALL REVIEWS\COMEDY REVIEWS.xlsx",9)


# In[3]:


#printing the dataframes to see the reviews 
r1_df 


# In[4]:


r2_df


# In[5]:


r3_df


# In[6]:


r4_df


# In[7]:


r5_df


# In[8]:


r6_df


# In[9]:


r7_df


# In[10]:


r8_df


# In[11]:


r9_df


# In[12]:


r10_df


# In[13]:


#combining all the review dataframes into one dataframe 
combined_df = pd.concat([r1_df, r2_df,r3_df,r4_df,r5_df,r6_df,r7_df,r8_df,r9_df,r10_df], ignore_index = True)


# In[14]:


combined_df


# In[15]:


#naming the column(s)
combined_df.columns=['transcript']


# In[16]:


# Let's take a look at the updated df
combined_df


# In[17]:


combined_df.sample(10)


# # Cleaning The Data
# When dealing with numerical data, data cleaning often involves removing null values and duplicate data, dealing with outliers, etc. With text data, there are some common data cleaning techniques, which are also known as text pre-processing techniques.
# 
# With text data, this cleaning process can go on forever. There's always an exception to every cleaning step. So, we're going to follow the MVP (minimum viable product) approach - start simple and iterate. Here are a bunch of things you can do to clean your data. We're going to execute just the common cleaning steps here and the rest can be done at a later point to improve our results.
# 
# ### Common data cleaning steps on all text:
# 
# - Make text all lower case
# - Remove punctuation
# - Remove numerical values
# - Remove common non-sensical text (\n-new lines,\t-whitespaces etc)
# - Tokenize text
# - Remove stop words
# ### More data cleaning steps after tokenization:
# 
# - Stemming / lemmatization
# - Parts of speech tagging
# - Create bi-grams or tri-grams
# - Deal with typos
# - And more...

# In[18]:


# Applying a first round of text cleaning techniques
import re
import string

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
   
    text = str(text)
    text = text.lower()

    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


# In[19]:


# Let's take a look at the updated text
data_clean_df = pd.DataFrame(combined_df.transcript.apply(clean_text_round1))
data_clean_df


# In[20]:


# Apply a second round of cleaning
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = str(text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text


# In[21]:


# Let's take a look at the updated text
data_clean_df = pd.DataFrame(data_clean_df.transcript.apply(clean_text_round2))
data_clean_df


# In[22]:


# Applying a third round of cleaning

import re
import string

text_translator = str.maketrans({ord(c): " " for c in string.punctuation})
def clean_text_round3(text, remove_punctuation_all=False):
    if not text:
        return ''
    try:
        text = text.replace(chr(160), " ")
        text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    except Exception as e:
        try:
            text = text.encode('utf-8')
            text = text.decode('utf-8')
        except Exception as e:
            return ""
    try:
        text = text.encode('ascii', 'ignore').decode("utf-8")
        text = text.translate(text_translator)
    except Exception as e:
        return ""
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return text


# In[23]:


# Let's take a look at the updated text
data_clean_df= pd.DataFrame(data_clean_df.transcript.apply(clean_text_round3))


# In[24]:


#Updated dataframe after three rounds of data cleaning
data_clean_df


# In[25]:


data_clean_df.sample(6)


# #### NOTE:  
# This data cleaning aka text pre-processing step could go on for a while, but we are going to stop for now. After going through some analysis techniques, if you see that the results don't make sense or could be improved, you can come back and make more edits such as:
# 
# - Mark 'cheering' and 'cheer' as the same word (stemming / lemmatization)
# - Combine 'thank you' into one term (bi-grams)
# - And a lot more...
# 
# 

# # Exploratory Data Analysis
# ### Introduction
# After the data cleaning step where we put our data into a few standard formats, the next step is to take a look at the data and see if what we're looking at makes sense. Before applying any fancy algorithms, it's always important to explore the data first.
# 
# When working with numerical data, some of the exploratory data analysis (EDA) techniques we can use include finding the average of the data set, the distribution of the data, the most common values, etc. The idea is the same when working with text data. We are going to find some more obvious patterns with EDA before identifying the hidden patterns with machines learning (ML) techniques. Let's look at the 
# - Most common words - find these and create word clouds
# 
# ## Organizing The Data
# The output of this notebook will be clean, organized data which can be done in two standard text formats:
# 
# 1. Corpus - a collection of text
# 2. Document-Term Matrix - word counts in matrix format
# 
# ### Corpus
# 
# The definition of a corpus is a collection of texts, and they are all put together.

# In[26]:


# Python program to generate WordCloud

 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 

comment_words = ''
stopwords = set(STOPWORDS)
 
# iterate through the combined dataframe file
for val in data_clean_df.transcript:
     
    # typecaste each val to string
    val = str(val)
 
   
      # split the value
    tokens = val.split()   
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()


# <b>Stopwords</b> are the English words which does not add much meaning to a sentence. They can safely be ignored without sacrificing the meaning of the sentence. For example, the words like the, he, have etc.
# 
# #### NOTE:
# At this point, we could go on and continue with this word clouds. However, by looking at these top words, you can see that some of them have very little meaning and could be added to a stop words list, so let's do just that.

# In[27]:


#present dictionary of stop words
print(stopwords)


# In[28]:


#corpus of our reviews
comment_words


# In[29]:


# Python program to find the most frequent words from data set
from collections import Counter
  

# split() returns list of all the words in the string
split_it = comment_words.split(" ")
  
  
# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common()
  
print(most_occur)


# In[30]:


# Excluding few words from the list
# Look at the most common top words --> add them to the stop word list

add_stop_words = [word for word, count in Counter.most_common() if count > 2135]
add_stop_words


# In[31]:


#adding more stopwords for better analysis
from sklearn.feature_extraction import text
additional_stop_words = text.ENGLISH_STOP_WORDS
print (additional_stop_words)


# In[32]:


# Python program to generate WordCloud
 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 

comment_words = ''

# Add new stop words

selected_stop_words=['show','season','one','season','watch','story','bajpayee','webserie','webseries','bajpai','manoj','episode','review','actor','actors']
stopwords = list(additional_stop_words) + selected_stop_words + add_stop_words + list(STOPWORDS)
 
# iterate through the file
for val in data_clean_df.transcript:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()    
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.title('Sentiment WorldCloud\n',fontsize=35)
plt.show()


# In[33]:


#all the stopwords that were used
print (stopwords)


# #### Findings
# We can clearly see that the word cloud has major chunk of positve reviews(roughly 75%) , some negative reviews (roughly 5%), with some neutral reviews(20%).
# 
# #### Let's dig into that and continue our analysis to back it up with statistical data.
# ### Side Note
# 
# What was our goal for the EDA portion? To be able to take an initial look at our data and see if the results of some basic analysis made sense.
# 
# Guess what? Yes,now it does, for a first pass. There are definitely some things that could be better cleaned up, such as adding more stop words or including bi-grams. But we can save that for another day. The results, especially to our objective make general sense, so we're going to move on.
# 
# As a reminder, the data science process is an interative one. It's better to see some non-perfect but acceptable results to help you quickly decide whether your project is inoperative or not.

# # Sentiment Analysis
# ## Introduction
# So far, all of the analysis we've done has been pretty generic - looking at counts, creating wordcloud plots, etc. These techniques could be applied to numeric data as well.
# 
# When it comes to text data, there are a few popular techniques that we may go through, starting with sentiment analysis. A few key points to remember with sentiment analysis.
# 
# 1. <b>TextBlob Module:</b> Linguistic researchers have labeled the sentiment of words based on their domain expertise. Sentiment of words can vary based on where it is in a sentence. The TextBlob module allows us to take advantage of these labels.
# 2. <b>Sentiment Labels:</b> Each word in a corpus is labeled in terms of polarity and subjectivity (there are more labels as well, but we're going to ignore them for now). A corpus' sentiment is the average of these.
# - <b>Polarity: </b>How positive or negative a word is. -1 is very negative. +1 is very positive.
# - <b>Subjectivity:</b> How subjective, or opinionated a word is. 0 is fact. +1 is very much an opinion.
# 
# For more info on how TextBlob coded up its sentiment function.(https://planspace.org/20150607-textblob_sentiment/)
# 
# Let's take a look at the sentiment of the various transcripts. 

# In[34]:


# Create quick lambda functions to find the polarity and subjectivity of each routine

from textblob import TextBlob

pol = lambda x: TextBlob(str(x)).sentiment.polarity
sub = lambda x: TextBlob(str(x)).sentiment.subjectivity

# Another way of writing the code , instead of using lambda parameter above.
''' 
def get_Subjectivity(text):
  return TextBlob(text).sentiment.subjectivity
def get_Polarity(text):
  return TextBlob(text).sentiment.polarity
  
  '''

data_clean_df['polarity'] = data_clean_df['transcript'].apply(pol)
data_clean_df['subjectivity'] = data_clean_df['transcript'].apply(sub)
data_clean_df


# In[35]:


data_clean_df.sample(5)


# In[36]:


#classifying sentiments based on the reviews'score
def get_analysis(score):
  if score > 0:
    return "positive"
  elif score < 0:
      return "negative"
  else: 
      return 'neutral'
data_clean_df["Analysis"] = data_clean_df.polarity.apply(get_analysis)
data_clean_df


# In[37]:


data_clean_df.sample(10)


# In[38]:


j=0
k=0
for i in range(0,data_clean_df.shape[0]):
    if data_clean_df.Analysis[i]=='negative':
       
        j= j+1
    elif data_clean_df.Analysis[i]=='positive':
#The folloswing code can be undocumented , if you're interested in reading that sentiments' reviews.
        #         print (k,data_clean_df.transcript[i])
        k+=1 
neu= data_clean_df.shape[0]- (j+k)        
print ('So,The following is our "Sentiment Analysis" for the Top 10 Indian Web Series(Comedy Genre) : ')
print ('\nNo of Negative Reviews from our Total DataSet(around 10k) ->',j) 
print ('No of Positive Reviews from our Total DataSet(around 10k) ->',k) 
print ('No of  Neutral Reviews from our Total DataSet(around 10k) ->',neu) 

neg_per= (j/data_clean_df.shape[0])*100
pos_per=(k/data_clean_df.shape[0])*100
neu_per=(neu/data_clean_df.shape[0])*100

print('\nPercentage of Negative Reviews -> '+ str(neg_per) + " %")
print('Percentage of Positive Reviews -> '+ str(pos_per) + ' %')
print('Percentage of Neutral  Reviews -> '+ str(neu_per) + "  %" )


# # Sentiment Findings:
# 
# #### So,The following is our "Sentiment Analysis" for the Top 10 Indian Web Series(Comedy Genre) : 
# 
# <pre>
# No of Negative Reviews from our Total DataSet(around 10k) -> 419
# No of Positive Reviews from our Total DataSet(around 10k) -> 6364
# No of  Neutral Reviews from our Total DataSet(around 10k) -> 1228
# 
# Percentage of Negative Reviews -> 5.230308326051679 %
# Percentage of Positive Reviews -> 79.44076894270378 %
# Percentage of Neutral  Reviews -> 15.328922731244537 %
# 
# 
# This also confirms our vague analysis that we did using just the wordcloud sentiments.<pre>

# # Data Visualizations
# 
# Data Visualization is the graphical representation of information and data. By using visual elements like charts, graphs, and maps, data visualization tools provide an accessible way to see and understand trends, outliers, and patterns in data.
# 
# #### The advantages and benefits of good data visualization
# 
# Our eyes are drawn to colors and patterns. We can quickly identify red from blue, square from circle. Our culture is visual, including everything from art and advertisements to TV and movies. Data visualization is another form of visual art that grabs our interest and keeps our eyes on the message. When we see a chart, we quickly see trends and outliers. If we can see something, we internalize it quickly. It’s basically storytelling with a purpose. 
# 
# ##### Other benefits of data visualization include the following:
# 
# - <b>Confirms our results derived from numeric data analysis.</b>
# - The ability to absorb information quickly, improve insights and make faster decisions;
# - An increased understanding of the next steps that must be taken to improve the organization;
# - An improved ability to maintain the audience's interest with information they can understand;
# - An easy distribution of information that increases the opportunity to share insights with everyone involved;
# - Eliminate the need for data scientists since data is more accessible and understandable; and
# - An increased ability to act on findings quickly and, therefore, achieve success with greater speed and less mistakes.

# In[39]:


# Let's plot the results
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [16, 12]

plt.scatter(data_clean_df['polarity'],data_clean_df['subjectivity'])
    
plt.title('Sentiment Analysis (Scatter Plot)', fontsize=30)
plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)

plt.show()


# In[40]:


plt.fill(data_clean_df['polarity'])
plt.title('Polarity of each Dataset', fontsize=30)
plt.xlabel('DataSets ( around 10K)', fontsize=15)
plt.ylabel('<-- Negative -------- Positive -->', fontsize=15)

plt.show()


# In[41]:


plt.fill(data_clean_df['subjectivity'])
plt.title('Subjectivity of each Dataset', fontsize=30)
plt.xlabel('DataSets ( around 10K)', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)

plt.show()


# In[42]:


plt.plot(data_clean_df['polarity'],data_clean_df['subjectivity'])
plt.rcParams['figure.figsize'] = [14, 10]    
plt.title('Sentiment Analysis (Line Plot)', fontsize=30)
plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)

plt.show()


# In[43]:


plt.plot(data_clean_df['polarity'])
plt.title('Polarity of each Dataset (Line Plot)', fontsize=30)
plt.xlabel('DataSets ( around 10K)', fontsize=15)
plt.ylabel('<-- Negative -------- Positive -->', fontsize=15)

plt.show()


# In[44]:


plt.plot(data_clean_df['subjectivity'])
plt.title('Subjectivity of each Dataset (Line Plot)', fontsize=30)
plt.xlabel('DataSets ( around 10K)', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)


plt.show()


# In[45]:


plt.hist(data_clean_df['polarity'], rwidth=.969)
plt.title('Polarity of each Dataset (Histogram)', fontsize=30)
plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
plt.ylabel('Frequency', fontsize=15)

plt.show()


# In[46]:


plt.hist(data_clean_df['subjectivity'], rwidth=.969)
plt.title('Subjectivity of each Dataset (Histogram)', fontsize=30)
plt.xlabel('<-- Facts -------- Opinions -->', fontsize=15)
plt.ylabel('Frequency', fontsize=15)

plt.show()


# In[47]:


data_clean_df


# In[48]:


#Creating a new DataFrame with only Positve Reviews. 
#We will later use this df to create a wordcloud having only positive sentiments. 
positive_df=data_clean_df[data_clean_df['Analysis']=='positive']


# In[49]:


positive_df


# In[50]:


# Python program to generate WordCloud for POSITVE SENTIMENTS
 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 

comment_words_pos = ''

# Add new stop words

selected_stop_words=['show','season','one','season','watch','story','web','character','episodes','bajpayee','bajpai','manoj','episode','review','actor','actors']
stopwords = list(additional_stop_words) + selected_stop_words + add_stop_words + list(STOPWORDS)
 
# iterate through the file
for val in positive_df.transcript:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()    
    comment_words_pos += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words_pos)
 
# plot the WordCloud image                      
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.title('WordCloud for POSITVE SENTIMENTS\n',fontsize=30)

plt.show()


# In[51]:


#Creating a new DataFrame with only Negatve Reviews. 
#We will later use this df to create a wordcloud having only negative sentiments. 
negative_df=data_clean_df[data_clean_df['Analysis']=='negative']


# In[52]:


negative_df


# In[63]:


# Python program to generate WordCloud for NEGATVE SENTIMENTS
 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 

comment_words_neg = ''

# Add new stop words

selected_stop_words=['show','season','one','good','funny','season','watch','character','characters','watching','story','bajpayee','bajpai','manoj','episode','review','actor','actors']
stopwords = list(additional_stop_words) + selected_stop_words + add_stop_words + list(STOPWORDS)
 
# iterate through the file
for val in negative_df.transcript:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()    
    comment_words_neg += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words_neg)
 
# plot the WordCloud image                      
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.title('WordCloud for NEGATVE SENTIMENTS\n',fontsize=30)

plt.show()


# In[54]:


#Creating a new DataFrame with only Neutral Reviews. 
#We will later use this df to create a wordcloud having only neutral sentiments. 
neutral_df=data_clean_df[data_clean_df['Analysis']=='neutral']


# In[55]:


# Python program to generate WordCloud for NEUTRAL SENTIMENTS
 
# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 

comment_words_neu = ''

# Add new stop words

selected_stop_words=['show','season','one','good','thriller','season','shame','watch','story','masterpiece','bajpayee','bajpai','manoj','episode','review','actor','actors']
stopwords = list(additional_stop_words) + selected_stop_words + add_stop_words + list(STOPWORDS)
 
# iterate through the file
for val in neutral_df.transcript:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()    
    comment_words_neu += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words_neu)
 
# plot the WordCloud image                      
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.title('WordCloud for NEUTRAL SENTIMENTS\n',fontsize=30)
 
plt.show()


# #### Additonal Information
# 
# The most frequent words from POSITIVE , NEGATIVE and NEUTRAL REVIEWS' data set.

# In[56]:


# Python program to find the most frequent words from POSITIVE REVIEWS' data set
from collections import Counter
  

# split() returns list of all the words in the string
split_it = comment_words_pos.split(" ")
  
  
# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common()
  
print(most_occur)


# In[57]:


# Python program to find the most frequent words from NEGATIVE REVIEWS' data set
from collections import Counter
  

# split() returns list of all the words in the string
split_it = comment_words_neg.split(" ")
  
  
# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common()
  
print(most_occur)


# In[58]:


# Python program to find the most frequent words from NEGUTRAL REVIEWS' data set
from collections import Counter
  

# split() returns list of all the words in the string
split_it = comment_words_neu.split(" ")
  
  
# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common()
  
print(most_occur)


# # THANK YOU
# ### - By Harsh Kumar ( Delhi Technological University,DTU (formerly Delhi College of Engineering,DCE))
# ### - Intern under Prof. Sasadhar Bera, Ph.D. (Indian Institute of Management ,Ranchi ) 
