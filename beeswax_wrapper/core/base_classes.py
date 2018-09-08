#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base Classes for the beeswax wrapper
Components in this module should not be used but built upon
"""
from __future__ import unicode_literals

from boltons.funcutils import wraps

from abc import ABCMeta, abstractproperty

from beeswax_wrapper.core.exceptions import BeeswaxRESTException


class BeeswaxABCMeta(ABCMeta):

    def __new__(mcs, name, bases, attrs):
        """Wrap methods in BeeswaxRestException raising"""
        for attr, pos_func in attrs.items():

            if callable(pos_func) and attr in {'retrieve', 'create', 'list', 'update', 'delete'}:
                attrs[attr] = BeeswaxABCMeta.wrap_errors(pos_func)

        return super(BeeswaxABCMeta, mcs).__new__(mcs, name, bases, attrs)

    @staticmethod
    def wrap_errors(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise BeeswaxRESTException(e)
        return new_func


class BaseAPI(object):
    """Base API class for attribute API structures"""
    __metaclass__ = BeeswaxABCMeta

    def __init__(self, dal):
        self._dal = dal

    @abstractproperty
    def paths(self):
        pass

    def _call(self, method, **kwargs):
        """Call to the DAL"""
        return self._dal.call(method, self.paths, **kwargs)