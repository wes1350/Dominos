class Config:
    def __init__(self, **kwargs):

        self.n_players = 4
        self.hand_size = 7
        self.win_threshold = 150
        self.check_5_doubles = True

        # initialize other parameters
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        self.validate_args()

    def validate_args(self):
        pass
