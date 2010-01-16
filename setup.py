try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='texcore',
    version='0.1.3',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "Genshi>=0.5.1",
        "nose>=0.11.1",
        "flup>=1.0.2"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'texcore': ['i18n/*/LC_MESSAGES/*.mo', 'fixtures/texglue.mk', 'fixtures/texmf/*/*/*/*']},
    #message_extractors={'texcore': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = texcore.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.server_runner]
    scgi_thread = texcore.lib.boot:run_scgi_thread
    """,
)
