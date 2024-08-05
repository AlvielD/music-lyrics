# Music Lyrics Ontology (ML)
This repository contains the content of our final project for Knowledge Engineering, tackling integration of lyrics data into the Polifonia music ontologies. You will find here the lyrics ontology module we created, the data we used with explanations on the way we obtained and standardized them, as well as the SPARQL queries used to create our Knowledge Graph.

> 🔗 Ontology URI [https://w3id.org/polifonia/ontology/music-lyrics/](https://raw.githubusercontent.com/Duam9/ke_final_project-july24/main/ontology/music-lyrics.rdf)

![](https://github.com/Duam9/ke_final_project-july24/blob/main/ontology/music-lyrics_grafoo.png)

https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2

Some problems we faced:
- lack of information about the song writers (need for API)
- lack of accessibility of interesting functions in API without commercial plans
- matching of lyrics when some are in lower case and other in cap letters
- find a common level of granularity for the two datasets
- encoding of characters between different alphabets
- translation of paragraph headers 
- no convention between different lyrics platforms for the spelling of interjections

Languages and files we put aside in the DALI dataset:
- because of encoding problems:
    - polish (75)
    - estonian (1)
    - croatian (4)
- because of too many hyphen in the text compared to Genius:
    - latin (1)

When converting the DALI json file to the final output file enriched with Genius info, we also detect asian languages and put them aside
because of asian characters being written the occidental way while the real asian characters are used in Genius

## Knowledge Graph Construction
Once the all our data was standardize into proper JSON files, we develop a SparQL construct query which allowed us to create the triples following the previously shown ontology. The whole model was build into this SparQL query and then binded the variables of each JSON datafile in order to triplify our data. The SparQL query file can be seen [here](https://github.com/Duam9/ke_final_project-july24/blob/main/sparql/populateOntology.sparql).