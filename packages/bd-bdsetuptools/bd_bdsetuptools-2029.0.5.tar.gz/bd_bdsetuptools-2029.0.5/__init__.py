try:
    from .setuo import amenda
except ImportError:
    from setup import amenda

amenda()

