import requests
import json
import pandas as pd


def national_holidays(country, api_key):
    """
    Parameters
    ----------
    country : string
        Country name. Must be in English language and start with capital letter.
        Check here for full list of supported countries: 
        https://calendarific.com/supported-countries
      
    api_key : string
        Valid calendarific API key. If you don't have an account, 
        you can sign up here: https://calendarific.com/signup 
    As of Feb 2023, there are 1000 free API requests/month.
      

    Returns 
    -------
    df_result : dataframe 
        Contains name, description and date of all 
        national holidays for the country passed as parameter.
    """

    #1 get data from csv and save in dataframe for data processing 
    # at a later stage and save country_list as a list
    df=pd.read_csv('/Users/usuario/national_holiday_pckg/natholi/natholi/country_list.csv')
   

    #find corresponding country code for country typed in by user
    for index, row in df.iterrows():
        if (df.at[index, 'country_name'] == country):
            country_code = df.at[index, 'iso-3166']
            print(country_code)

    # api call
    # api documentation
    # https://calendarific.com/api-documentation
    holidays = requests.get(f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country_code}&year=2023").text

    # get json with results
    results_js = json.loads(holidays)
    print(results_js)

    # keep only json data that is of interest
    data2 = results_js['response']['holidays']
    print(data2)

    # convert it into dataframe
    # full dataframe
    df_full_results = pd.DataFrame.from_records(data2)
    # dataframe with only name and description columns
    df_selected_results = df_full_results[['name', 'description']]
    # issue with date format, making a dataframe with iso date only
    df_dates=pd.DataFrame.from_records(df_full_results['date'])
    df_dates.rename(columns={'iso': 'date'},inplace=True)
    df_date=df_dates['date']

    # final dataframe with name, desc and date
    df_result = pd.concat([df_selected_results, df_date], axis=1)

    return df_result