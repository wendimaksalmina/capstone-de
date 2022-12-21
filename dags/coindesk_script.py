def store_coindesk_to_bq():
    from google.oauth2 import service_account
    import requests
    import pandas
    import pandas_gbq
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()

    df = pandas.DataFrame()
    # add diclaimer column to dataframe
    df['disclaimer'] = [data['disclaimer']]
    # add chartname column to dataframe
    df['chart_name'] = [data['chartName']]
    # add updated time column to dataframe
    df['time_updated'] = [data['time']['updated']]
    # add updateISO time column to dataframe
    df['time_updated_iso'] = [data['time']['updatedISO']]
    # add code column to dataframe
    df['bpi_usd_code'] = [data['bpi']['USD']['code']]
    # add eur code column to dataframe
    df['bpi_eur_code'] = [data['bpi']['EUR']['code']]
    # add gbp code column to dataframe
    df['bpi_gbp_code'] = [data['bpi']['GBP']['code']]
    # add usd rate column to dataframe
    df['bpi_usd_rate'] = [data['bpi']['USD']['rate']]
    # add eur rate column to dataframe
    df['bpi_eur_rate'] = [data['bpi']['EUR']['rate']]
    # add gbp rate column to dataframe
    df['bpi_gdp_rate'] = [data['bpi']['GBP']['rate']]
    # add usd description column to dataframe
    df['bpi_usd_description'] = [data['bpi']['USD']['description']]
    # add eur description column to dataframe
    df['bpi_eur_description'] = [data['bpi']['EUR']['description']]
    # add gbp description column to dataframe
    df['bpi_gdp_description'] = [data['bpi']['GBP']['description']]
    # add usd rate_float column to dataframe
    df['bpi_usd_rate_float'] = [data['bpi']['USD']['rate_float']]
    # add eur rate_float column to dataframe
    df['bpi_eur_rate_float'] = [data['bpi']['EUR']['rate_float']]
    # add gbp rate_float column to dataframe
    df['bpi_gdp_rate_float'] = [data['bpi']['GBP']['rate_float']]
    # add bpi_idr_rate_float column to dataframe which conveted from usd rate_float
    df['bpi_idr_rate_float'] = [data['bpi']['USD']['rate_float'] * 15000]
    # convert column time_updated and time_updated_iso to strftime('%Y-%m-%d %H:%M:%S')
    df['time_updated'] = pandas.to_datetime(df['time_updated']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['time_updated_iso'] = pandas.to_datetime(df['time_updated_iso']).dt.strftime('%Y-%m-%d %H:%M:%S')
    # add last_updated column to dataframe
    df['last_updated'] = pandas.to_datetime('now', utc=True).tz_convert(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S')
    #print df head
    # df.head()
    #set credentials
    credentials = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": "secure-cipher-366713",
            "private_key_id": "449d1fbbaf5921f8551b00d08b30d21e61670e57",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDlzeN2apaRGG0+\nlkJVo9lWTxoCPBKQXj0tws2Eo+oqye9CFRWyDpNIApNoDlmL5spiJzRDEAJhqtcn\n6p88JV0nTux617S/TC2UPqSyaw7Dy/dP1N78bBTmFUfTdMlJjlCsTJhVmlqZXtr8\nfWaxQejwSFzJzpC7m/yPk7ih6wXy+WYqrVdiRPL3b7X3H8aaNF9OTYBsOC/e87Se\n8GMHjh5sp50HuBkCb5wOlvX8ZSa45180ruhDdNznGzyab4PhwP3b/kyCz42qYTCw\n07MJeobvXH2bwyq6uG5b098L+6rcpRAPbb96QMUhz6NlAgLFZjgoXMiflwio1u9l\nUkO6XZ85AgMBAAECggEAIbWld7Hj+02/fK5S9bgOwgvhb1F7kaTZSZSpTBs1Vuh/\nSczI/XEI5sfF8r4kIZMNvf8tOecnykbiv865Y/vBIeqAYvawY11b1EKqKyfsJwmM\n8i9yNEnweN3HRvv7KOiQ6e1kbS4yuwvAiMgmX7sg3dpnjgzYi0Sy9CbBrzLIER+A\nVd/TuSLIPtEAj2j/2lpO8/4pGn7sOoyuc3TcjOjA6c1/7yzg5uuMSn56oDq8AYUS\npKKqGKPTtFQ9weocrCGkp1lOzraWe5nLnFkhf2PcOY02Nj2Ub1l5+5irODvo7OIg\n/eTMxOYPupfP1Wrqrl/PvNmg+/Q3rtugyOjiM3behwKBgQDy9+Hr6dZFgG9HaWYD\nHyByYCFy2MjD/Mm3s0aDeuoo6A3zbtekVs+rYzE45UidU24KvxDxbvjoTFnFDPnH\neEL9TRSbWAiPLPmhu4D1qckB/5vm7bkvV2lxHufPLfIWOifSaEKC4njCJjlq7CC0\nal2J2WcGasxcjPyjX9ojIRjg2wKBgQDyIUFDyzxZ/jEPYhQprKFpZo9MLVMmBb44\nMYsraKgC7J3FOGdzVLwl7UVas/zoglnqmk3N1uw94kvsXu3HN5E79Hbjqznk2q3k\n1W2jrRGDui0OQnZl7u2LRrsfVAPFbMo6rukE0A2oL7L4ApK4eoXtroJaHELENMvH\nvV28Hg2iewKBgGDOYzWb9cO7aJsLY5nazRLFOo6H0XZFQhnvVCkO0D18OBLGFyVj\ncVrYKsSAlm4Yz794YUfQ71ufECVzBhJz2D0UeSFr8f0Z7lyCWN+Ixo4FShi4nxA9\nw8VOiw4BQHOauEMdR2Le2T6B/F6dtmor9xj1hhcIdmRpyD9P8ZoNldwBAoGAWSRl\nItBwJ7Gt3jv9sFoeEu/vUdxeAGGc5pNW6WRedrUmYLWjYJKRsmToY7xgIDndYMHu\nYxn9X8swqJVKdU2/6pLWMnuXlOntm5H4C4psKFMiw100udJ9IgmoWqBTwxuKWJCM\nuXjfjkwBV82attBk/lyBISvGaPYHEEJngBqQaoECgYEA5+JMnVYnmcAZ34mhrf+5\n82/ymjwFX3Y8rK2NhuB/ITOZUd3FzqaNVZOdxYc0LtOukIYGabzAfl8dy6D9qPVp\n12Qv/m3mxEqFhR/QTlabj2VEgmJDf/sf/asnfXOCpEx7Zd0J9mCK+7Dk8YyGCG6U\nMqJfkbHjdw+ZlHb7ijxeXTI=\n-----END PRIVATE KEY-----\n",
            "client_email": "secure-cipher-366713@appspot.gserviceaccount.com",
            "client_id": "118412656588707664000",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/secure-cipher-366713%40appspot.gserviceaccount.com"
        },
    )
    # load dataframe to bigquery
    pandas_gbq.to_gbq(df, 'capstone_data_engineer.coindesk', project_id="secure-cipher-366713", if_exists='replace', credentials=credentials)