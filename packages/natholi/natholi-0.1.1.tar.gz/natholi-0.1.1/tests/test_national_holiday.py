from natholi.national_holiday import national_holidays
import pandas as pd
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/national_holiday_pckg')
load_dotenv(os.path.join(project_folder, 'natholi/.env'))

CALENDARIFIC_API_KEY=os.getenv("CALENDARIFIC_API_KEY")

def test_national_holidays(): 
    val0 = national_holidays('Algeria', f"{CALENDARIFIC_API_KEY}").iloc[0,0]
    assert val0=="New Year"

    val1 = national_holidays('Algeria', f"{CALENDARIFIC_API_KEY}").iloc[1,0]
    assert val1=="Berber New Year"