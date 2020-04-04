from SPARQLWrapper import SPARQLWrapper, JSON


def make_wd_ids_str(qids: list):
    wd_prefixed = {f'wd:{qid}' for qid in qids}
    wd_ids_str = ' '.join(wd_prefixed)
    return wd_ids_str


def get_results(endpoint_url, query):
    user_agent = 'country-levels/0.1 (https://github.com/hyperknot/country-levels)'
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()
