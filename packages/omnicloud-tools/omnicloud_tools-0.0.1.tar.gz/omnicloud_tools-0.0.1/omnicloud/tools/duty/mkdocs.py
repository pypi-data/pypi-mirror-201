'''
'''

from duty import duty


__all__ = [
    'mkdocs_run',
    'mkdocs_req'
]


@duty
def mkdocs_req(ctx):
    '''
    Export MkDocs requirements from poetry's mkdocs group to .docs/.mkdocs.req file.
    '''

    ctx.run(
        'poetry export --without-hashes --only mkdocs --no-cache --output .docs/.mkdocs.req',
        title="Export MkDocs requirements to .docs/.mkdocs.req file"
    )


@duty(pre=[mkdocs_req])
def mkdocs_run(ctx):
    '''
    Build & Serv the [MkDocs Documentation](https://www.mkdocs.org/) on 0.0.0.0:8008.
    '''

    ctx.run(
        'mkdocs build --config-file .docs/.mkdocs.yml --site-dir ../.html',
        title='Building documentation'
    )

    ctx.run(
        'mkdocs serve --config-file .docs/.mkdocs.yml --dev-addr 0.0.0.0:8008',
        title='Serving on http://localhost:8008/'
    )
