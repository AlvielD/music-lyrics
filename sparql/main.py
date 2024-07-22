import pysparql_anything as sa

def main():
    engine = sa.SparqlAnything()
    engine.run(
            query="sparql/populateOntology.sparql",
            format="ttl",
            values={
                "filePath" : "ontology/music-lyrics.rdf",
                "fileName" : "music-lyrics"
            }
        )

    return

if __name__ == '__main__':
    main()