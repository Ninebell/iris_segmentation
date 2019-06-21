import argparse


def make_parser():
    parser = argparse.ArgumentParser("find iris segment use Daughman's algorithm\n you need radius and eye image.")
    parser.add_argument('--r', type=int, help='iris radius, Do not bigger than image width, height!')
    parser.add_argument('--p', help='image folder path')
    parser.add_argument('--e', help='image extension. ex) bmp')
    return parser


def get_radius(parser):
    return parser.parse_args().r


def get_path(parser):
    return parser.parse_args().p


def get_extension(parser):
    return parser.parse_args().e

