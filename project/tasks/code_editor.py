from celery import shared_task
from django.conf import settings
from docker import from_env as docker_client

from api import models


EDITOR_CONFIG_TEMPLATE = '''
bind-addr: 127.0.0.1:8080
auth: password
password: {password}
cert: false
'''

@shared_task
def start(user_id: int):
    user = models.User.objects.get(id=user_id)

    user_project = user.directory / 'project/'
    user_configs = user.directory / '.config/'
    code_server_configs = user_configs / 'code-server/'
    user_editor_config = code_server_configs / 'config.yaml'

    user_project.mkdir(parents=True, exist_ok=True)
    code_server_configs.mkdir(parents=True, exist_ok=True)

    if not user_editor_config.exists():
        with user_editor_config.open(mode='w') as f:
            f.write(EDITOR_CONFIG_TEMPLATE.format(password=user.login))

    docker = docker_client()
    editor_containers = docker.containers.list(all=True, filters={'name': user.editor_name})

    if editor_containers:
        editor_container = editor_containers[0]

        if editor_container.status == 'exited':
            editor_container.start()

        return user.editor_port

    docker.containers.run(
        'dimastark/code-editor',
        detach=True,
        name=user.editor_name,
        ports={
            f'8080/tcp': user.editor_port,
        },
        volumes={
            str(user_configs.absolute()): dict(bind='/home/coder/.config', mode='rw'),
            str(user_project.absolute()): dict(bind='/home/coder/project', mode='rw'),
        },
    )

    return user.editor_port


@shared_task
def stop(user_id: int):
    user = models.User.objects.get(id=user_id)

    docker = docker_client()
    editor_containers = docker.containers.list(filters={'name': user.editor_name})

    if not editor_containers:
        return

    editor_containers[0].stop()


def status(user_id: int):
    user = models.User.objects.get(id=user_id)

    docker = docker_client()
    editor_containers = docker.containers.list(filters={'name': user.editor_name})

    if not editor_containers:
        return 'exited'

    return editor_containers[0].status
