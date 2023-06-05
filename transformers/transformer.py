class Transformer:
    def __init__(self, job) -> None:
        self.job = job

    def __getattr__(self, __name: str):
        try:
            return self.job[__name]
        except KeyError:
            return None
