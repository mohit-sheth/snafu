import elasticsearch
import os
import sys
import datetime
import string 
import random

def _json_payload(uuid, test_type, test_name, routes, conn_per_targetroute, keepalive, tls_reuse, delay, runtime, requests_per_second, latency_95pctl, timestamp_newyork):
    processed = []
    processed.append({
        "uuid" : uuid,
        "test_type" : test_type,
        "test_name" : test_name,
        "routes" : routes,
        "conn_per_targetroute" : conn_per_targetroute,
        "keepalive" : keepalive,
        "tls_reuse" : tls_reuse,
        "delay" : delay,
        "runtime" : runtime,
        "requests_per_second" : requests_per_second,
        "latency_95pctl" : latency_95pctl,
        "timestamp_newyork" : timestamp_newyork
    })
    return processed

def _index_result(index, server, port, payload):
    _es_connection_string = str(server) + ':' + str(port)
    es = elasticsearch.Elasticsearch([_es_connection_string], send_get_body_as='POST')
    print(es)
    for result in payload:
        print(result)
        es.index(index=index, body=result)

def main():
    
    server = os.environ["ES_SERVER"]
    port = os.environ["ES_PORT"]
    test_name = os.environ["HTTP_TEST_SUFFIX"]
    test_type = os.environ["test_type"]
    routes = os.environ["routes"]
    conn_per_targetroute = os.environ["conn_per_targetroute"]
    keepalive = os.environ["keepalive"]
    tls_reuse = os.environ["tls_reuse"]
    delay = os.environ["delay"]
    runtime = os.environ["runtime"]
    requests_per_second = os.environ["requests_per_second"]
    latency_95pctl = os.environ["latency_95pctl"]
    timestamp_newyork = datetime.datetime.now()
    uuid = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 37)) 

    documents = _json_payload(uuid, test_type, test_name, routes, conn_per_targetroute, keepalive, tls_reuse, delay, runtime, requests_per_second, latency_95pctl, timestamp_newyork)
    print(documents)
    if len(documents) > 0:
        _index_result("router-test-results", server, port, documents)


if __name__ == '__main__':
    sys.exit(main())



