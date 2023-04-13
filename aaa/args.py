import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str)
    print(parser)
    args = parser.parse_args()
    print(args)
    print(args.name)
