from setuptools import find_packages
from setuptools import setup

setup(
    name="insight_python_linux",
    author="htsc",
    version="4.2.1",
    author_email="insight@htsc.com",
    description="insight_python_linux",
    long_description="insight_python_linux",
    license='insightpythonsdk',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },

    packages=['insight_python',
              'insight_python/com',
              'insight_python/com/interface',
              'insight_python/com/cert',
              'insight_python/com/insight',

              'insight_python/com/libs/linux/python36',
              'insight_python/com/libs/linux/python37',
              'insight_python/com/libs/linux/python39',
              'insight_python/com/libs/linux/python310',

              ],

    package_dir={
                 'insight_python/com/cert': 'insight_python/com/cert',
                 'insight_python': 'insight_python',
                 'insight_python/com/libs/linux/python36':
                     'insight_python/com/libs/linux/python36',
                 'insight_python/com/libs/linux/python37':
                     'insight_python/com/libs/linux/python37',
                 'insight_python/com/libs/linux/python39':
                     'insight_python/com/libs/linux/python39',
                 'insight_python/com/libs/linux/python310':
                     'insight_python/com/libs/linux/python310',
                 },

    package_data={
        'insight_python/com/cert': ['HTInsightCA.crt', 'InsightClientCert.pem', 'HTISCA.crt', 'InsightClientKeyPkcs8.pem'],
        'insight_python': ['requirements.txt'],
        'insight_python/com/libs/linux/python36': ['_mdc_gateway_client.so', 'libACE.so.6.4.3', 'libACE_SSL.so.6.4.3', 'libprotobuf.so.11',
                                                "libmdc_query_client.so", "mdc_gateway_client.py",
                                                "libcrypto.so.1.0.2k", "libcrypto.so.10", "libssl.so", "libssl.so.1.0.2k",
                                                "libssl.so.10", "libssl3.so"],
        'insight_python/com/libs/linux/python37': ['_mdc_gateway_client.so', 'libACE.so.6.4.3', 'libACE_SSL.so.6.4.3', 'libprotobuf.so.11',
                                                "libmdc_query_client.so", "mdc_gateway_client.py",
                                                "libcrypto.so.1.0.2k", "libcrypto.so.10", "libssl.so", "libssl.so.1.0.2k",
                                                "libssl.so.10", "libssl3.so"],
        'insight_python/com/libs/linux/python39': ['_mdc_gateway_client.so', 'libACE.so.6.4.3', 'libACE_SSL.so.6.4.3', 'libprotobuf.so.11',
                                                "libmdc_query_client.so", "mdc_gateway_client.py",
                                                "libcrypto.so.1.0.2k", "libcrypto.so.10", "libssl.so", "libssl.so.1.0.2k",
                                                "libssl.so.10", "libssl3.so"],
        'insight_python/com/libs/linux/python310': ['_mdc_gateway_client.so', 'libACE.so.6.4.3', 'libACE_SSL.so.6.4.3', 'libprotobuf.so.11',
                                                "libmdc_query_client.so", "mdc_gateway_client.py",
                                                "libcrypto.so.1.0.2k", "libcrypto.so.10", "libssl.so", "libssl.so.1.0.2k",
                                                "libssl.so.10", "libssl3.so"],

        },

    install_requires=[],

    python_requires='>=3.6.*',
)