def update_tag_counters(redis_client, tags):
    pipe = redis_client.pipeline()
    for tag in tags:
        counter_key = create_key_from_tag(tag)
        pipe.incr(counter_key)
    pipe.execute()
