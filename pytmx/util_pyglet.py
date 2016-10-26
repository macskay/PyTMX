"""
Copyright (C) 2012-2016

This file is part of pytmx.

pytmx is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pytmx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pytmx.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

logger = logging.getLogger(__name__)

try:
    import pyglet
except ImportError:
    pyglet = None
    logger.error('cannot import pyglet (is it installed?)')
    raise

__all__ = ('load_pyglet', 'pyglet_image_loader')


def load_pyglet(filename, *args, **kwargs):
    """ Load a map and images for pyglet

    The invert_y kwarg is set to True automatically.

    :param filename:
    :param args:
    :param kwargs:

    :rtype: pytmx.TiledMap
    """
    import pytmx

    kwargs['image_loader'] = pyglet_image_loader
    kwargs['invert_y'] = True
    return pytmx.TiledMap(filename, *args, **kwargs)


def pyglet_image_loader(filename, colorkey, **kwargs):
    """ Basic image loading with pyglet

    returns pyglet Images, not textures

    This is a basic proof-of-concept and is likely to fail in some situations.

    Missing:
        Transparency
        Tile Rotation

    This is slow as [hw]ell
    """
    if colorkey:
        logger.debug('colorkey not implemented')

    image = pyglet.image.load(filename)

    def load_image(rect=None, flags=None):
        if rect:
            try:
                x, y, w, h = rect
                y = image.height - y - h
                tile = image.get_region(x, y, w, h)
            except:
                logger.error('cannot get region %s of image', rect)
                raise
        else:
            tile = image

        if flags:
            logger.error('tile flags are not implemented')

        return tile

    return load_image
