from setuptools import find_packages, setup

def packages():
    return [
        'yt_dlp_cp', 'yt_dlp_cp.extractor', 'yt_dlp_cp.downloader', 'yt_dlp_cp.postprocessor', 'yt_dlp_cp.compat',
    ]

setup(
        name='yt-dlp-cp',
        version='0.0.7',
        maintainer='kylin99999',
        maintainer_email='kylinwork@yeah.net',
        packages=packages(),
    )
