'''
'''

from os import environ as env

from duty import duty


__all__ = [
    'gcp_login'
]


@duty
def gcp_login(ctx):
    '''
    Login to Google Cloud Platform.
    Tried to read project_id from $GCP_PROJECT
    '''

    ctx.run(
        'gcloud beta auth login --update-adc --enable-gdrive-access --add-quota-project-to-adc --brief',
        title='Login'
    )

    project = env.get('GCP_PROJECT', None) or input('Please enter GCP project id: ')
    ctx.run(
        f'gcloud config set project {project}',
        title='Set project'
    )
