from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Return all Property objects from cache if available,
    otherwise fetch from DB and store in Redis for 1 hour.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # cache 1 hour
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics: keyspace_hits, keyspace_misses, hit ratio.
    """
    # Get raw Redis client from django-redis
    client = cache.client.get_client()

    # Get Redis stats
    stats = client.info('stats')
    hits = stats.get('keyspace_hits', 0)
    misses = stats.get('keyspace_misses', 0)
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0

    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': hit_ratio
    }

    # Log metrics
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics