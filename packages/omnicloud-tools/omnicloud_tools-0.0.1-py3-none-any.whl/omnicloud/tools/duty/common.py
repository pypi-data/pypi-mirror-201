'''
'''

from duty import duty


__all__ = [
    'clean',
]


@duty
def clean(ctx):
    '''
    Clean up the project directory.
    '''

    ctx.run(
        'rm -rf .html || true',
        title="Remove .html folder"
    )
    ctx.run(
        'rm -f poetry.lock || true',
        title="Remove poetry.lock file"
    )
    ctx.run(
        'rm -rf dist || true',
        title="Remove dist folder"
    )


@duty
def lab_dev(ctx):
    """Run the ./lab/index.py as a developer."""
    ctx.run(
        'python3 .lab/index.py',
        title='Run the app in development mode on 8008'
    )


@duty
def lab_run(ctx):
    """Run the ./lab/run.sh like a production."""
    ctx.run(
        'bash .lab/run.sh',
        title='Run the app in production mode on 8008'
    )
