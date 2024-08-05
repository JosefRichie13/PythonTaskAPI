import html
import datetime
import re

# Sanitizes the string to avoid XSS vulnerabilities
# Also removes any double spaces in between the strings
def sanitizeString(inputString):
    santizedString = html.escape(inputString)
    santizedString = re.sub(' +', ' ', santizedString)
    return santizedString



# Checks if the date format is in DD-MMM-YYYY format, e.g. 23-May-2053
# Returns TRUE if its in the format or FALSE if its not
def checkDateFormat(inputDate):
    try:
        datetime.datetime.strptime(inputDate, "%d-%b-%Y")
        return True
    except:
        return False
