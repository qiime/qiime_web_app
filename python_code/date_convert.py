
def us_to_everyone(date_list):
    """ Converts dates in US format (mm/dd/yyyy) to international format (dd/mm/yyyy)
    """
    if not date_list:
        raise Exception('Date list not provided')
    
    converted_dates = []
    for d in date_list:
        month, day, year = d.split('/')
        converted = '{0}/{1}/{2}'.format(day, month, year)
        print converted
        converted_dates.append(converted)
                
    return converted_dates
    
def everyone_to_us(date_list):
    """ Converts dates in internation format (dd/mm/yyyy) to US (mm/dd/yyyy)
    """
    if not date_list:
        raise Exception('Date list not provided')
        
    converted_dates = []
    for d in date_list:
        day, month, year = d.split('/')
        converted = '{0}/{1}/{2}'.format(month, day, year)
        print converted
        converted_dates.append(converted)
                
    return converted_dates
