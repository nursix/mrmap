from celery import shared_task


@shared_task(name="async_analyze_log", priority=3,)
def async_analyze_log(http_response_log_id, **kwargs):
    from registry.models.security import AnalyzedResponseLog, HttpResponseLog
    http_response_log = HttpResponseLog.objects.get(pk=http_response_log_id)
    analyzed_response_log = AnalyzedResponseLog(response=http_response_log)
    analyzed_response_log.analyze_response()
    analyzed_response_log.save()
    return True
