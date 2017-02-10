from datetime import datetime


class Logging(object):

    @staticmethod
    def get_tstamp():
        return str(datetime.utcnow())[0:19]

    @classmethod
    def log(cls, msg):
        print("{0}: {1}".format(cls.get_tstamp(),  msg))

    @classmethod
    def log_to_file(cls, msg):
        with open('deploy.log', 'a') as file:
            file.write("{0}: {1}".format(cls.get_tstamp(),  msg))
            file.flush()
            file.close()


if __name__ == '__main__':
    Logging.log('whatever')