import dill


def main():
    with open('data/model.bin', 'rb') as f:
        predictor = dill.load(f)
    print(predictor.predict(['google.com']))


if __name__ == '__main__':
    main()
