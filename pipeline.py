import logging
import subprocess
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logger.info('Starting extract process')
    subprocess.run(['python3', 'main.py'], cwd='./extract')
    logger.info('Extract process finished!')

def _transform():
    logger.info('Starting transform process')
    subprocess.run(['python3', 'main.py'], cwd='./transform')
    logger.info('Transform process finished!')

def _load():
    subprocess.run(['python3', 'main.py'], cwd='./load')
    logger.info('Process finished!')

if __name__ == '__main__':
    main()
