# Music Lyrics Ontology (ML)
This repository contains the content of our final project for Knowledge Engineering, tackling integration of lyrics data into the Polifonia music ontologies. You will find here the lyrics ontology module we created, the data we used with explanations on the way we obtained and standardized them, as well as the SPARQL queries used to create our Knowledge Graph.

> 🔗 Ontology URI [https://w3id.org/polifonia/ontology/music-lyrics/](https://raw.githubusercontent.com/Duam9/ke_final_project-july24/main/ontology/music-lyrics.rdf)

![](https://github.com/Duam9/ke_final_project-july24/blob/main/ontology/music-lyrics_grafoo.png)

## Competency Questions

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

## Data JSONification
In order to triplify the data it was needed a previous step involving cleaning and standarziation of data from different sources. We made use of [DALI](https://github.com/gabolsgabs/DALI) and [DAMP](https://ccrma.stanford.edu/damp/) datasets for audio aligned data, while additional information was completed with the help of [Spotify](https://developer.spotify.com/documentation/web-api) and [Genius](https://docs.genius.com/) APIs.

- [Tutorial on lyrics web scraping](https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2)

Lyrics are carefully encoded and decoded usin UTF-8, then they are cleaned from extra data written by the users and aligned with the lyrics extracted from [Genius](https://genius.com/).

When converting the DALI json file to the final output file enriched with Genius info, we also detect asian languages and put them aside
because of asian characters being written the occidental way while the real asian characters are used in Genius

## Knowledge Graph Construction
Once the all our data was standardize into proper JSON files, we develop a SparQL construct query which allowed us to create the triples following the previously shown ontology. The whole model was build into this SparQL query and then binded the variables of each JSON datafile in order to triplify our data. The SparQL query file can be seen [here](https://github.com/Duam9/ke_final_project-july24/blob/main/sparql/populateOntology.sparql).

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

## Possible Improvements
The scope of this project is to give an entry point to extend the polifonia ontology on the audio-aligned data. There are many things to be done yet:
- Improve the cleaning in order to get more songs from the DAMP dataset.
- Perform the entity linking on the Polifonia knowledge graph.
- Enhance the granularity to syllable level.
- Extend the artist field to all artists involved in the writting process
- Add the dataset source information
