from functions.create_pandas_df import create_df


def test():
    art_df = create_df("./data/tf_vdibart.csv")
    print("Result for tf_vdibart:")
    print(art_df.head())

if __name__=="__main__":
    test()