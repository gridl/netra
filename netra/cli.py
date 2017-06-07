import sys
from os.path import expanduser
import urllib.request

import click
import numpy as np
from PIL import Image

from netra import MNIST_IMAGE_DIMENSIONS
from netra.regression import Regression
from netra.rnn import LSTM
from netra.utils import get_logger


logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--model_name', '-m', default=None,
              help='Specify model to train. Available models: regression, lstm.')
def train(model_name):
    """
    Train available models.
    """
    if not model_name:
        logger.info('Specify model to train. Available models: regression, lstm.')

    MODELS = {Regression.NAME: Regression, LSTM.NAME: LSTM}
    MODEL = MODELS.get(model_name, None)

    if not MODEL:
        logger.info('Invalid model specified. Available models: regression, lstm.')
        sys.exit()

    m = MODEL()
    m.train()


@cli.command()
@click.option('--image', '-i', default=None,
              help='Specify image to test.')
def query(image):
    if image.startswith(('http://', 'https://')):
        img = Image.open(urllib.request.urlopen(image))
    else:
        img = Image.open(expanduser(image))
    img = img.convert("L")
    img.thumbnail(MNIST_IMAGE_DIMENSIONS, Image.ANTIALIAS)
    data = np.asarray(img.getdata()).reshape(1, 784)
    data = (data / 255)
    # from pprint import pprint; pprint(data)
    model = Regression()
    model.query(data)