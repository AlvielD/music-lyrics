# Music Lyrics Ontology and Knowledge Graph (ML)
This repository contains the content of our final project for Knowledge Engineering, tackling integration of lyrics data into the Polifonia music ontologies. You will find here the lyrics ontology module we created, the data we used with explanations on the way we obtained and standardized them, as well as the SPARQL queries used to create our Knowledge Graph.

## How to use this repository
### Files hierarchy
.
├── conversion/
│   ├── config
│   ├── saved
│   ├── test
│   ├── dali_avoided_songs.txt
│   ├── GeniusCompiler.py
│   ├── header_synonyms.txt
│   ├── id.txt
│   ├── LyricsAnnot.py
│   ├── main.py
│   ├── real_conversion.ipynb
│   ├── test_conversion.ipynb
│   ├── SongNotFoundException.py
│   ├── SpotiScraper.py
│   ├── test_conversion.ipynb
│   ├── translation.py
│   └── utils.py
├── ontology/
│   ├── catalog-v001.xml
│   ├── music-lyrics.rdf
│   └── music-lyrics_grafoo
├── sparql/
│   ├── annotations
│   ├── triples
│   ├── populateOntology.ipynb
│   ├── populateOntology.sparql
│   └── queries.ipynb
├── .gitignore
├── READ_ME
├── Requirements
├── use_dataset.ipynb
└── utils.py

### Advices
We advise you to read the whole current file and the annotated notebooks that are referred along the way before trying to use its content on your own.<br>
Don't forget to move to the main folder and run pip install -r Requirements.txt to be able to run the scripts.

## Steps 
## Design of the Ontology
First of all, we designed an ontology that our knowledge graph has to respect. We made sure to link it to some [Polifonia](https://github.com/polifonia-project/ontology-network/?tab=readme-ov-file) already-existing modules (mostly Core and Music Meta) when the information we wanted to display were already present in them.
> 🔗 Ontology URI [https://w3id.org/polifonia/ontology/music-lyrics/](https://raw.githubusercontent.com/Duam9/ke_final_project-july24/main/ontology/music-lyrics.rdf)

You can visualize it here:
![](https://github.com/Duam9/ke_final_project-july24/blob/1619f87e8833be1538766d1c6d1cb6d623cb7993/ontology/music-lyrics_grafoo.png)


### Competency Questions
We designed our ontology so that the data created according to it can answer the following questions:

| **ID** | **Competency question**                                                  | **Reference** |
|--------|--------------------------------------------------------------------------|---------------|
| 1      | Who is the primary artist involved in the creative process of a song?    | Music Meta    |
| 2      | In what language is written a song?                                      | Core          |
| 3      | Which different languages the lyrics from our Knowledge Graph use?       | Core          |
| 4      | Which are the different sections of a song?                              | Music Lyrics  |
| 5      | What are the lyrics associated to an specific section of a song?         | Music Lyrics  |
| 6      | What are the starting and ending time stamps of a specific lyric's line? | Music Lyrics  |
| 7      | What is the duration of a lyric's line?                                  | Music Lyrics  |
| 8      | What is the duration of a song's section?                                | Music Lyrics  |
| 9      | What are the singers in charge of singing a specific song's section?     | Music Lyrics  |

If you want to take try to query through our knowledge graph to retrieve these answers, here is the notebook that will guide you step by step to perform this:


## Data preparation

The current version of ChoCo contains 20,080 JAMS files: 2,283 from the audio partitions, and 17,803 collected from symbolic music.
In turn, these JAMS files provide 60263 different annotations: 20,530 chord annotations in the Harte notation, and 20,029 annotations of tonality and modulations -- hence spanning both local and global keys, when available.
Besides the harmonic content, ChoCo also provides 554 structural annotations (structural segmentations related to music form) and 286 beat annotations (temporal onsets of beats) for the audio partitions.

| **Partition**        | **Type** | **Notation**  | **Original format** | **Annotations**  | **Genres** |  **References**  |
|----------------------|----------|---------------|---------------------|------------------|------------|:----------------:|
| Isophonics           | A        | Harte         | LAB                 | 300              | pop, rock  |        [1]       |
| JAAH                 | A        | Harte         | JSON                | 113              | jazz       |        [2]       |
| Schubert-Winterreise | A, S     | Harte         | csv                 | 25 (S), 25*9 (A) | classical  |        [3]       |
| Billboard            | A        | Harte         | LAB, txt            | 890 (740)        | pop        |        [4]       |
| Chordify             | A        | Harte         | JAMS                | 50*4             | pop        |        [5]       |
| Robbie Williams      | A        | Harte         | LAB, txt            | 61               | pop        |        [6]       |
| The Real Book        | S        | Harte         | LAB                 | 2486             | jazz       |        [7]       |
| Uspop 2002           | A        | Harte         | LAB                 | 195              | pop        |        [8]       |
| RWC-Pop              | A        | Harte         | LAB                 | 100              | pop        |        [9]       |
| Weimar Jazz Database | A        | Leadsheet     | SQL                 | 456              | jazz       |       [10]       |
| Wikifonia            | S        | Leadsheet     | mxl                 | 6500+            | various    |       [11]       |
| iReal Pro            | S        | Leadsheet     | iReal               | 2000+            | various    |       [12]       |
| Band-in-a-Box        | S        | Leadsheet     | mgu, sku            | 5000+            | various    |       [13]       |
| When in Rome         | S        | Roman         | RomanText           | 450              | classical  |       [14]       |
| Rock Corpus          | S        | Roman         | har                 | 200              | rock       |       [15]       |
| Mozart Piano Sonata  | S        | Roman         | DCMLab              | 54 (18)          | classical  |       [16]       |
| Jazz Corpus          | S        | Hybrid        | txt                 | 76               | jazz       |       [17]       |
| Nottingham           | S        | ABC           | ABC                 | 1000+            | folk       |       [18]       |

The average duration of the annotated music pieces is $191.29 \pm 85.04$ seconds for (audio) tracks, and $135.02 \pm 162.27$ measures for symbolic music.
This provides a heterogeneous corpus with a large extent of variability in the duration of pieces, which also confirms the diversity of musical genres in ChoCo.
Additional statistics can be found from [this](https://github.com/smashub/choco/blob/main/notebooks/dataset_stats.ipynb) Jupyter notebook.


## Data preparation
### Choice of the datasets
To create a knowledge graph, we first need some data.<br>
Since we wanted to work with audio-aligned lyrics, we decided after some investigation to use the two following datasets:
- [DALI](https://github.com/gabolsgabs/DALI);
- [DAMP](https://ccrma.stanford.edu/damp/).
We then had to enrich these data with more details, among them the paragraph information. To perform this, we used both of these API:
- [Genius](https://docs.genius.com/);
- [Spotify](https://developer.spotify.com/documentation/web-api).
Here is one of the tutorials that helped us to scrape the lyrics from the web using the API: 
[Tutorial on lyrics web scraping](https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2)

### Choice of the output format
Then, we had to converge on the output format. We chose JSON as it is a simple basic structured format, and that the datasets we were using were quite simple to convert in json (the lyrics files were already json ones in DAMP, and in DALI there were some built-in functions to convert their files to json).

### Choice of the output content


### Cleaning of the data

### Data JSONification
In order to triplify the data it was needed a previous step involving cleaning and standarziation of data from different sources. We made use of [DALI](https://github.com/gabolsgabs/DALI) and [DAMP](https://ccrma.stanford.edu/damp/) datasets for audio aligned data, while additional information was completed with the help of [Spotify](https://developer.spotify.com/documentation/web-api) and [Genius](https://docs.genius.com/) APIs.



Lyrics are carefully encoded and decoded using UTF-8, then they are cleaned from extra data written by the users and aligned with the lyrics extracted from [Genius](https://genius.com/).

When converting the DALI json file to the final output file enriched with Genius info, we also detect asian languages and put them aside because of asian characters being written the occidental way while the real asian characters are used in Genius

## Knowledge Graph Construction
Once all of our data was standardized into proper JSON files, we develop a SparQL construct query which allowed us to create the triples following the previously shown ontology. The whole model was build into this SparQL query and then binded the variables of each JSON datafile in order to triplify our data. The SparQL query file can be seen [here](https://github.com/Duam9/ke_final_project-july24/blob/main/sparql/populateOntology.sparql).

Generated triples can be checked [here](https://github.com/Duam9/ke_final_project-july24/tree/main/sparql/triples).

## Faced Problems
- Lack of information about the song writers (need for API)
- Lack of accessibility of interesting functions in API without commercial plans
- Matching of lyrics when some are in lower case and other in cap letters
- Find a common level of granularity for the two datasets
- Encoding of characters between different alphabets
- Translation of paragraph headers 
- No convention between different lyrics platforms for the spelling of interjections

Languages and files we put aside in the DALI dataset:
- because of encoding problems:
    - polish (75)
    - estonian (1)
    - croatian (4)
- because of too many hyphen in the text compared to Genius:
    - latin (1)

## Conclusion
We are very happy to have been able to concretely used what we had studied in class in such an ambitious project, despite the short time we had to complete it.<br>
The scope of this project is to give an entry point to extend the Polifonia ontology on the audio-aligned data. There are hence many things to be done still. Here are some improvement axis:
- Improve the cleaning in order to get more songs from the DAMP dataset;
- Perform the entity linking on the Polifonia knowledge graph;
- Enhance the granularity to syllable level.
- Extend the artist field to all artists involved in the writing process;
- Add the dataset source information in the ontology and complete the knowledge graph accordingly.
