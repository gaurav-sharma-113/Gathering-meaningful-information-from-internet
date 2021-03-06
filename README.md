# Getting links of webpages containing relevant information from the internet

The goal of the project is to list out articles from the web which talk about a particular topic. Here I am trying to get a list of URLs which contain information about economic impact of covid.

The methodology tried in this project is as follows:

## Access through common crawl archive
The data used is from **October'2020** from the commoncrawl repository (https://commoncrawl.org/2020/11/october-2020-crawl-archive-now-available/).

## Processing the textual data
Two approaches were followed in this case.
First was to get the textual content of the webpage using **Beautiful Soup** module following which the HTML content of the text was preprocessed by replacing email addresses, weblinks and other symbols except for alphabets and numbers using generic tokens (like 'emailaddr', 'httpaddr', 'dollar').
After this, the cleaned data was used to find if the words "Covid" or "Corona" and "Economic" or "Economy" were present in the clean text. 
The second methodology used was to summarise the textual data and extract 5 sentences from the text of the data and then use the conditions mentioned above to find if the articles contained information about "Economic impact of covid". 

***How was summarisation done?***

This could be done in 2 ways:

The first approach followed was based on the term frequency and adding them up to find the "weight" of the sentence. The most important ("weighted") sentences were then returned as the summary of the text. 

There is another method which could be used (could not be implemented entirely and hence not included due to paucity of time) to get this summarization which is done via NetworkX module's pagerank method. Here, we form a matrix (which is later considered as adjacency matrix of the graph) based on "1-cosine_score" of 2 sentences in a text. This means perfectly similar sentence would have a score of 1, and entirely different sentences will have a score of 0. Now, based on this PageRank function computes a ranking of the nodes in the graph (described by the adjacency matrix calculated before) and returns the most important sentences which are then used as summary of the text given.

**Result**
The result is a list of url which contain this information of economic impact of covid 19. A score list is also maintained in order to keep a check on the number of URLs that are required to be stored. This can serve as a marker for stopping point for the algorithm. Here, score is incremented by 1 if a URL being considered is found to be relevant. I use this score as 1000, i.e. I stop the algorithm when I get 1000 URLs containing the relevant information. The URLs are in the file FinalURL.txt


### How to use:

1. Run the command in the terminal : ```bash ./create_venv.sh```
2. After this, a virtual environment will be created and required components will be installed from ```requirements.txt```
3. There are 2 files being used in the code, hence to run the code, the command should be : ```python main.py```
4. Output will be the scores and names of the variables that contain the url

*(If at all there is an error for the model "en_core_web_sm", please run the following command in the terminal:*

*pip install spacy*

*python3 -m spacy download en_core_web_sm)*

(There is also a script available to run on the grid ```test_gpu.sh``` which could be run directly without having to go through any of the steps above)

