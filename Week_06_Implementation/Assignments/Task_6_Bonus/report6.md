# Report 6

I would find the target method by name, then combine code search and embeddings to collect its class, dependencies and tests. I would choose context by relevance and token budget rather than always taking five chunks.

Large classes could be split into methods. After generation, the pipeline would check the changes, run tests and use failures for repairs. The pricing repair showed why dependencies matter: it worked after the model received the Money definition. This improved pipeline is a proposal.
