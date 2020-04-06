from loguru import logger
import numpy as np
from scipy.spatial.distance import cdist

from tokenizer import Tokenizer
from vectorizer import Vectorizer


def _get_token_similarity(query_string, pred_string):
    query_tokens = Tokenizer.tokenize(query_string)
    pred_tokens = Tokenizer.tokenize(pred_string)
    pred_vec = dict(zip(pred_tokens, Vectorizer.vectorize_tokens(pred_tokens)))
    query_vec = dict(zip(query_tokens, Vectorizer.vectorize_tokens(query_tokens)))
    ret = {}
    for k,v in query_vec.items():
        dist = cdist([v], np.stack( list(pred_vec.values()), axis=0 ), metric='cosine')[0]
        idx = dist.argsort()[:2]
        ret.update({k:list(np.asarray(list(pred_vec.keys()))[idx])})
    return ret

def get_most_similar_title(query_title, df, top_n=5):
    logger.info(f"Query: \t\t {query_title}")
    v0, tokens = Vectorizer.vectorize_sent(query_title, get_tokens=True)
    logger.info(f"Processed Query: {' '.join(tokens)}\n")
    dist = cdist([v0], np.stack( df.title_vect.values, axis=0 ), metric='cosine')[0]
    idx = dist.argsort()[:top_n]
    values = df[["title", "abstract", "publish_time", "authors", "journal", "source_x", "url"]].loc[idx].to_dict("records")
    ret = dict({"query":query_title, "processed_query":' '.join(tokens), "pred":{}})
    for n, i , each in zip(range(1,top_n+1), idx, values):
        tok_sim = _get_token_similarity(" ".join(tokens), each["title"])
        ret["pred"].update({
            n: {
                "score":round((1.0 - dist[i]),5),
                "title": each["title"], 
                "abstract":each["abstract"],
                "publish_time":each["publish_time"],
                "authors":each["authors"],
                "journal":each["journal"],
                "source_x":each["source_x"],
                "url":each["url"],
#                 "token_similarity":tok_sim
            }
        })
    return ret
