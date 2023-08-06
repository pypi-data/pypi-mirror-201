from persiantools.jdatetime import JalaliDate
import datetime


def get_date(persian=True, folder_path=False):
    """This function retrns current date, wheter in shamsi or miladi.

    :param persian: A bolean value determining the foramt of date (in shamsi or miladi), defaults to True
    :type persian: bool, optional
    :param folder_path: A boolean value determining if the date will be used as a folder name or not, defaults to False
    :type folder_path: bool, optional
    :return: Current date
    :rtype: string
    """
    # persian date
    if persian:
        # get day
        day = str(JalaliDate.today().day)
        if len(day)==1:
            day = '0' + day
        #
        # get month
        month = str(JalaliDate.today().month)
        if len(month)==1:
            month = '0' + month
        #
        # full date string
        if not folder_path:
            date = '%s/%s/%s' % (JalaliDate.today().year, month, day)
        else:
            date = '%s-%s-%s' % (JalaliDate.today().year, month, day)

    # miladi date
    else:
        # get day
        day = str(datetime.datetime.today().date().day)
        if len(day)==1:
            day = '0' + day
        #
        # get month
        month = str(datetime.datetime.today().date().month)
        if len(month)==1:
            month = '0' + month
        #
        # full date string
        if not folder_path:
            date = '%s/%s/%s' % (datetime.datetime.today().date().year, month, day)
        else:
            date = '%s-%s-%s' % (datetime.datetime.today().date().year, month, day)

    return date

def get_time(folder_path=False):
    """This function returns current time.

    :param folder_path: A boolean value determining if the date will be used as a folder name or not, defaults to False
    :type folder_path: bool, optional
    :return: Current time
    :rtype: string
    """

    time = datetime.datetime.now()
    
    if not folder_path:
        time = str(time.strftime("%H:%M:%S"))
    else:
        time = str(time.strftime("%H-%M-%S"))
    
    return time

def get_datetime(persian=True, folder_path=True):
    """This function returns both curent date and time in wheater shamsi or miladi format.

    :param persian: A bolean value determining the foramt of date (in shamsi or miladi), defaults to True
    :type persian: bool, optional
    :param folder_path: A boolean value determining if the date will be used as a folder name or not, defaults to True
    :type folder_path: bool, optional
    :return: Current date and time
    :rtype: string
    """
    
    date = get_date(persian=persian, folder_path=folder_path)
    time = get_time(folder_path=folder_path)

    return date + "-" + time

def get_days_per_month(month=1, persian=True):
    """This function returns number of days for a given month.

    :param month: Month that we want to get number of its days, defaults to 1
    :type month: int, optional
    :param persian: A bolean value determining the foramt of date (in shamsi or miladi), defaults to True
    :type persian: bool, optional
    :return: Number of days for given month
    :rtype: int
    """
    assert 1 <= month <= 12, "month should be between 1 and 12"
    if persian:
        if month <= 6:
            return 31
        else:
            return 30
    else:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        if month == 2:
            return 29
        return 30

    
