class getLg:
    val = '';

    def __init__(self, caller_file_name):
        self.val = caller_file_name
        print("created by " + caller_file_name)
        print('val : ' + self.val)

    def __del__(self):
        print("destroyed...")


def gggg(input: str):
    print ("gggg is called by " + input)


