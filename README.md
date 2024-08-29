# Music Lyrics Ontology and Knowledge Graph (ML)
This repository contains the content of our final project for Knowledge Engineering, tackling integration of lyrics data into the Polifonia music ontologies. You will find here the lyrics ontology module we created, the data we used with explanations on the way we obtained and standardized them, as well as the SPARQL queries used to create our Knowledge Graph.

## How to use this repository
### Files hierarchy
![](https://github.com/AlvielD/music-lyrics/blob/PW_KE/assets/Files_hierarchy.PNG)

### Advices
We advise you to read the whole current file and the annotated notebooks that are referred along the way before trying to use its content on your own.<br>
Don't forget to move to the main folder and run pip install -r Requirements.txt to be able to run the scripts.

## Steps 
## Design of the Ontology
First of all, we designed an ontology that our knowledge graph has to respect. We made sure to link it to some [Polifonia](https://github.com/polifonia-project/ontology-network/?tab=readme-ov-file) already-existing modules (mostly Core and Music Meta) when the information we wanted to display were already present in them.
> 🔗 Ontology URI [https://w3id.org/polifonia/ontology/music-lyrics/](https://raw.githubusercontent.com/AlvielD/music-lyrics/PW_KE/ontology/music-lyrics.rdf)

You can visualize it here:
![](https://github.com/AlvielD/music-lyrics/blob/PW_KE/ontology/music-lyrics_grafoo.png)


### Competency Questions
We designed our ontology so that the data created according to it can answer the following questions:

| **ID** | **Competency question**                                                  | **Reference** |
|--------|--------------------------------------------------------------------------|---------------|
| 1      | In what language is written a song?                                      | Core          |
| 2      | Which different languages the lyrics from our Knowledge Graph use?       | Core          |
| 3      | Who is the primary artist involved in the creative process of a song?    | Music Meta    |
| 4      | What are all the different artists involved in writing the lyrics?       | Music Meta    |
| 5      | Which are the different sections of a song?                              | Music Lyrics  |
| 6      | What are the lyrics associated to an specific section of a song?         | Music Lyrics  |
| 7      | What are the starting and ending time stamps of a specific lyric's line? | Music Lyrics  |
| 8      | What is the duration of a lyric's line?                                  | Music Lyrics  |
| 9      | What is the duration of a song's section?                                | Music Lyrics  |
| 10     | What are the singers in charge of singing a specific song's section?     | Music Lyrics  |
| 11     | What is the dataset where the annotations were taken from?               | Music Lyrics  |
| 12     | From which dataset was extracted each JSON data file?                    | Music Lyrics  |

If you want to take try to query through our knowledge graph to retrieve these answers, you can find [here](https://github.com/AlvielD/music-lyrics/blob/PW_KE/sparql/queries.ipynb) a notebook that will guide you step by step to perform this.



## Data preparation
### Choice of the datasets
To create a knowledge graph, we first needed some data.<br>
Since we wanted to work with audio-aligned lyrics, we decided after some investigation to use the two following datasets:
- [DALI](https://github.com/gabolsgabs/DALI);
- [DAMP](https://ccrma.stanford.edu/damp/).<br>
These datasets provide us with lyrics splitted (either in paragraphs, in lines, in words or even in notes) along with time indexes for start and end of the lyrics fragment.<br>
We then had to enrich these data with more details, among them the paragraph information. To perform this, we used both of these API:
- [Genius](https://docs.genius.com/);
- [Spotify](https://developer.spotify.com/documentation/web-api).<br>
Here is one of the tutorials that helped us to scrape the lyrics from the web using the API: 
[Tutorial on lyrics web scraping](https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2)

### Choice of the output format
Then, we had to converge on the output format. We chose JSON as it is a simple basic structured format, and that the datasets we were using were quite simple to convert in json (the lyrics files were already json ones in DAMP, and in DALI there were some built-in functions to convert their files to json).

### Choice of the output content
We designed our output content's structure and fields so that it provides us with the information we will need to create our knwoledge graph according to our ontology. It is at this step that we decided to not go below the lines granularity level for lyrics: indeed, DAMP randomly contains either notes or lines, while DALI always contains both, in addition to words and paragraphs!<br>
The thing is, if we have a song which audio alignment is represented line by line in DAMP, we could maybe find out how to split the words of the lines into syllables, but we would not have the related time tags of each syllables. So we thought it was better to focus on a scale a bit larger, hence line by line.

You can look at the structure of a converted file [here](https://raw.githubusercontent.com/AlvielD/music-lyrics/PW_KE/conversion/saved/00000000.json).


### Cleaning of the data
Since we had to match the dataset file's content with the [Genius](https://genius.com/)'s content to be able to form the paragraphs, many kind of mistakes could lead to a mismatch. We incrementally improved our system by implementing cleaning functions.<br>
Here is a summary of the different obstacles we had to overcome:
- Matching of lyrics when some are in lower case and other in cap letters
- Encoding of characters between different alphabets:
<br>We had to put aside all the polish songs (75), the estonian (1) and the croatian ones (4) from DALI dataset because the encoding was wrong in the source file.
<br>We also had to put aside the asian songs from DALI dataset because they were written in occidental characters while the Genius ones were in asian characters (so no possibility for successful matching).
- Translation of paragraph headers:
<br>We implemented english to be the standard, that required us to create a [translation dictionary](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/header_synonyms.py).
- No convention between different lyrics platforms for the spelling of interjections or for the adlibs:
<br>We had to use functions matching the longest substring (cf. in [utils.py](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/utils.py)) instead of absolute comparison ones.

### Data JSONification
Once that we had well planned and implemented everything, we were ready to carry out the whole conversion. You can follow the preparatory steps we did in the [test_conversion](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/test_conversion.ipynb) notebook.<br>
The successful results obtained after this preliminary step then led us to use the bulk functions defined in [main.py](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/main.py) and then perform some post-conversion steps so as to obtain out final dataset folder. You can follow these steps in the [real_conversion](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/real_conversion.ipynb) notebook.
<br><br>
During the conversion, lyrics are carefully encoded and decoded using UTF-8, then they are cleaned from extra data written by the users and aligned with the lyrics extracted from [Genius](https://genius.com/).
<br>
When converting a dataset json file to the final output file enriched with [Genius](https://genius.com/)'s info, we have to be careful when assigning an ID to it: this one should be unique, and enable to prevent having duplicates if a song is present in both datasets. We took care of this thanks to an [id text file](https://raw.githubusercontent.com/AlvielD/music-lyrics/PW_KE/conversion/id.txt) updated and referred to along the way.<br>
We also detect the songs that have problems and skip them while listing them in the avoided_file folder along with a skipping reason. Due to unexpected overwriting problems while converting DAMP, we unfortunately did not get its avoided songs' list, but we got it for DALI.<br>
Theoretically, here are the reasons possible to skip a song (depending on the entry dataset):
<br>
| DALI | DAMP |
| :----------------: | :----------------: |
| no_paragraphs [on Genius] | no_paragraphs [on Genius] |
| no_language_information [on Genius] | no_language_information [on Genius] |
| not_found_on_Genius | not_found_on_Genius | 
| wrongly_encoded_asian_song | notes_encoding_instead_of_lines | 
<br>

### Our Dataset
We advise you to take a look at the DALI and DAMP statistics presented in the second part of the [real_conversion](https://github.com/AlvielD/music-lyrics/blob/PW_KE/conversion/real_conversion.ipynb) notebook. Here is a small summary:

| **Dataset**        | Number of usable converted songs | Number of avoided songs  | Percentage of usability |
|----------------------|:--------:|:-------------:|:-------------------:|
| DALI           | 3051       |   1885*      | 61.81%***                | 
| DAMP           | 1115        |   3834*        | 29.08%***                 | 

## Knowledge Graph Construction
Once all of our data was standardized into proper JSON files, we develop a SparQL construct query which allowed us to create the triples following the previously shown ontology. The whole model was build into this SparQL query and then binded the variables of each JSON datafile in order to triplify our data. The SparQL query file can be seen [here](https://github.com/Duam9/ke_final_project-july24/blob/main/sparql/populateOntology.sparql).

Generated triples can be checked [here](https://github.com/AlvielD/music-lyrics/tree/PW_KE/sparql/triples).

## SparQL endpoint
The SparQL endpoint is available to be build locally through a Fuseki server. To do so, follow the steps below

1. First, create a new dataset by clicking on `new dataset`. It will take some time, so we suggest to store it in a persistent format ( $\approx$ 15Gb).
2. Then, click on `add data`.
3. Select the `.ttl` files on the **triples** folder and `upload all`.

Once the process is done you can query the Knowledge Graph on http://localhost:3030/#/dataset/<dataset_name>/query.

Keep in mind you need Java 17 or more to execute the version of Fuseki present on this repository. There shouldn't be any problems if you try downloading an older version of Fuseki server, but we haven't tested them.


## Conclusion
We are very happy to have been able to concretely use what we had studied in class in such an ambitious project, despite the short time we had to complete it.<br>
The scope of this project is to give an entry point to extend the Polifonia ontology on the audio-aligned data. There are hence many things to be done still.<br>
Here are some improvement axis:
- Improve the cleaning in order to get more songs from the DAMP dataset;
- Perform the entity linking on the Polifonia knowledge graph;
- Enhance the granularity to syllable level.
