from setuptools import setup

setup(
    name='funke_enrichment_core',
    version='1.21.3',
    author='Friedrich Schmidt',
    author_email='friedrich.schmidt@funkemedien.de',
    packages=['funke_enrichment_core'],
    scripts=[],
    license='MIT',
    description='This package contains everthing to orchestrate several microservices in the GCP',
    install_requires=[
        'aiohttp-retry',
        'requests',
        'asyncio',
        'google_cloud_bigquery',
        'pandas',
        'pyarrow',
        'firebase-admin',
        'google-cloud-secret-manager',
        'google-cloud-pubsub',
        'python-dateutil'
    ]
)