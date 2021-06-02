# Search Engine
- Capable of handling tens of thousands of documents or Web pages, under harsh operational constriants and having a query response time under 300ms

## Indexer
Create an inverted index for the corpus with the following:
  - Tokens: all alphanumeric sequences in the dataset.
  - Stop words: does not use stopping while indexing, i.e.  use all words, even the frequently occurring ones.
  - Stemming: uses stemming for better textual matches (Porterstemming)
  - Important text:  text in bold (b, strong), in headings (h1, h2, h3), and in titles are treated as more important than the in other places. Verifies the relevant HTML tags to select the important words.

## Search
Utilizes the inverted index for document retrieval with boolean queries. Documents sorted based on tf-idf score and cosine similarity. Optimized index that runs both the indexer and the search with small memory footprint, smaller than the index size.
