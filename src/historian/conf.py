import os

broker_url = 'amqp://guest@{0}//'.format(os.environ['BROKER_HOST'])
result_backend = 'amqp://guest@{0}//'.format(os.environ['BROKER_HOST'])

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_annotations = {
    'tasks.add': {'rate_limit': '5/m'}
}
