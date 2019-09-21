def update_tag_counters(redis_client, tags):
    for tag in tags:
        counter_key = create_key_from_tag(tag)
        redis_client.incr(counter_key)
