import os

broker_url = 'amqp://guest@{0}//'.format(os.environ['BROKER_MACHINE'])
result_backend = 'amqp://guest@{0}//'.format(os.environ['BROKER_MACHINE'])

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_annotations = {
    'tasks.add': {'rate_limit': '5/m'}
}
