#!/usr/bin/env python

"""
command line builder for nls auto configure

"""

import argparse
def cmdbuild(cmdname=None):
    def build(cls):
        if cmdname:
            CMDBuilder.CATEGORIES[cmdname]=cls
        else:
            CMDBuilder.CATEGORIES[cls.__name__.lower()]=cls
        return cls
    return build

class CMDBuilder(object):
    CATEGORIES = {}

    def __init__(self):
        pass
    @staticmethod
    def cmdbuild(cmdname=None):
        def build(cls):
            if cmdname:
                CMDBuilder.CATEGORIES[cmdname]=cls
            else:
                CMDBuilder.CATEGORIES[cls.__name__.lower()]=cls
            return cls
        return build

    @staticmethod
    def Args(*args,**kwargs):
        def _decorator(func):
            func.__dict__.setdefault('args', []).insert(0, (args,kwargs))
            return func
        return _decorator

    @staticmethod
    def run(subcommand=False):
        top_parser = argparse.ArgumentParser(prog='top')
        subparsers = top_parser.add_subparsers()
        for category in CMDBuilder.CATEGORIES:
            command_object = CMDBuilder.CATEGORIES[category]()
            if subcommand:
                category_parser = subparsers.add_parser(category)
                category_parser.set_defaults(command_object=command_object)
                subparsers = category_parser.add_subparsers(dest='action')
            for (action, action_fn) in methods_of(command_object):
                subparser = subparsers.add_parser(action)
                action_kwargs = []
                for args, kwargs in getattr(action_fn, 'args', []):
                    subparser.add_argument(*args, **kwargs)
                subparser.set_defaults(action_fn=action_fn)
            #parser.set_defaults(action_kwargs=action_kwargs)
        match_args = top_parser.parse_args()
        fn = match_args.action_fn
        fn(*fetch_func_args(fn, match_args))

def methods_of(obj):
    result = []
    for i in dir(obj):
        if callable(getattr(obj, i)) and not i.startswith('_'):
            result.append((i, getattr(obj, i)))
    return result

def fetch_func_args(func,matchargs):
    fn_args = []
    for args, _ in getattr(func, 'args', []):
        arg = args[0]
        if arg.startswith('--'):
            arg = arg[2:]
        elif arg.startswith('-'):
            arg = args[1][2:]
        fn_args.append(getattr(matchargs, arg))
    return fn_args


if __name__ == "__main__":
    top_parser = argparse.ArgumentParser(prog='top')
    subparsers = top_parser.add_subparsers()

    for category in CMDBuilder.CATEGORIES:
        command_object = CMDBuilder.CATEGORIES[category]()

        category_parser = subparsers.add_parser(category)
        category_parser.set_defaults(command_object=command_object)

        category_subparsers = category_parser.add_subparsers(dest='action')
        for (action, action_fn) in methods_of(command_object):
            parser = category_subparsers.add_parser(action)

            action_kwargs = []
            for args, kwargs in getattr(action_fn, 'args', []):
                parser.add_argument(*args, **kwargs)
            parser.set_defaults(action_fn=action_fn)
            #parser.set_defaults(action_kwargs=action_kwargs)
    match_args = top_parser.parse_args()
    fn = match_args.action_fn
    fn(*fetch_func_args(fn, match_args))
