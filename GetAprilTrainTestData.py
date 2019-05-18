def GetAprilTrainTestData():

    import pandas as pd
    import numpy as np
    import time
    import datetime

    ssr_raw_df = pd.read_csv("data/SSR_Apr2019_TrainTestData.csv", 
                        dtype={"USP_REV" : str, "TESTERSUBTYPE" : str })


    # X is the first 50 columns. MSYE and MSYE_RULE are Y. Going to try 
    # regression with the variable data first. 
    # Drop all columns that have NaN in them - should figure out why and be sure it is fixed going forward. 
    # Though actually, the GUIDs should only be for combining data from tables, not learning about it. Same with dates. 
    # Until I figure out how to look at serial data for trends

    # Make any adjustments to the raw SSR data pulled
    ssr_df = ssr_raw_df.loc[(ssr_raw_df["LOTSCREENTYPE"] == "FIRST_PASS") & (ssr_raw_df["TEST_AREA"] == "FT1")].copy()
    ssr_df.drop(["SEG_GUID", "PGM_GUID"], axis=1, inplace=True)
    ssr_df.drop(["SETUP_START_DATE"], axis=1, inplace=True)    # , "SETUP_END_DATE" removed for time based training
    ssr_df.drop(["TTAPAG", "TESTERCONFIG", "PKG", "LBID"], axis=1, inplace=True)

    # Adds a column and populates it with Unix time (seconds since 1/1/1970)
    utime_ser = []
    for i,row in ssr_df.iterrows():
        tstr = row["SETUP_END_DATE"]
        pt=time.mktime(datetime.datetime.strptime(tstr[:len(tstr)-2], "%Y-%m-%d %H:%M:%S").timetuple())
        utime_ser.append(pt)
    ssr_df["UTIME"] = utime_ser

    ssr_df.sort_values(["TESTERTYPE", "TESTER", "UTIME"], inplace = True)


    return ssr_df;
    

