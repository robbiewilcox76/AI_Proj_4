import pickle

class Data:
 
    @staticmethod
    def load_object(filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)

    @staticmethod
    def save_data(data, filename):
        try:
            with open(filename, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)