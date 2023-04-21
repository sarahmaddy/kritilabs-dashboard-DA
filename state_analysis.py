
def state_call_analysis(call_file,trip_file,states,months,years):
    #import statements
    import os
    from datetime import datetime
    from datetime import timedelta
    import pandas as pd
    #reading the files which are given as input 
    call_df=pd.read_csv(call_file)
    trip_df=pd.read_csv(trip_file)
    call_df.rename(columns = {'Comapny Name':'Company Name'}, inplace = True)
    # data - pre processsing
    call_df["Company Name"].replace("EXMI customer","EXMI customer-EXMI customer" ,inplace=True)
    call_df["Company Name"].replace("Kritilabs Test","Kritilabs Test-Kritilabs Test",inplace=True )

    trip_df.rename(columns = {'Company':'Company Name'}, inplace = True)

    trip_df["Company Name"].replace("EXMI customer","EXMI customer-EXMI customer" ,inplace=True)
    trip_df["Company Name"].replace("Kritilabs Test","Kritilabs Test-Kritilabs Test",inplace=True )

    call_df["State"]=call_df["Company Name"].apply(lambda x:x.split("-")[-2])

    call_df["Date"]=pd.to_datetime(call_df['Call Date & Time'],dayfirst=True).apply(lambda x: x.date())
    call_df["Date"]=call_df["Date"].apply(lambda x:datetime.strftime(x,"%d-%m-%Y"))
    call_df["Date"]=pd.to_datetime(call_df['Date'],dayfirst=True).apply(lambda x: x.date())

    #call_df["Month"]=call_df["Date"].apply(lambda x:x.split("-")[1])
    #call_df["Year"]=call_df["Date"].apply(lambda x:x.split("-")[2])
    call_df["Month"]=call_df["Date"].apply(lambda x:x.month)
    call_df["Year"]=call_df["Date"].apply(lambda x:x.year)

    trip_df["State"]=trip_df["Company Name"].apply(lambda x:x.split("-")[-2])
    trip_df["Date"]=pd.to_datetime(trip_df['Start Time'],dayfirst=True).apply(lambda x: x.date())
    trip_df["Date"]=trip_df["Date"].apply(lambda x:datetime.strftime(x,"%d-%m-%Y"))
    trip_df["Date"]=pd.to_datetime(trip_df['Date'],dayfirst=True).apply(lambda x: x.date())

    ##trip_df["Month"]=trip_df["Date"].apply(lambda x:x.split("-")[1])
    ##trip_df["Year"]=trip_df["Date"].apply(lambda x:x.split("-")[2])

    trip_df["Month"]=trip_df["Date"].apply(lambda x:x.month)
    trip_df["Year"]=trip_df["Date"].apply(lambda x:x.year)

    def month_conv(num):
        months=["Jan","Feb","March","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
        return months[num-1]

    #converting month  numbers to month names :
    call_df['Month']=call_df['Month'].apply(lambda x:month_conv(x))
    trip_df['Month']=trip_df['Month'].apply(lambda x:month_conv(x))

    call_df=call_df[["Company Name","Vehicle Number","Network Operator","Call Date & Time","State","Date","Month","Year","Invoice number","Problem","Location name"]]




    calldata=call_df[(call_df["State"].isin(states))& (call_df["Month"].isin(months)) & (call_df["Year"].isin(years))]
    tripdata=trip_df[(trip_df["State"].isin(states))& (trip_df["Month"].isin(months)) & (trip_df["Year"].isin(years))]

    call_data=calldata.groupby(["State","Month","Year"]) 
    trip_data=tripdata.groupby(["State","Month","Year"])

  #ANALYSIS BEGINS 
    state_call_data={}
    state_trip_data={}
    for state in states:
        for index,year in enumerate(years):
            if index==0:
                state_call_data[state]={}
                state_call_data[state][year]={}
                state_trip_data[state]={}
                state_trip_data[state][year]={}
            for index1,month in enumerate(months):
                if index1==0:
                    state_call_data[state][year][month]={}
                    state_trip_data[state][year][month]={}
                try:
                    state_call_data[state][year][month]=call_data.get_group((state,month,year))
                except:
                    state_call_data[state][year][month]=""

                try:
                    state_trip_data[state][year][month]=trip_data.get_group((state,month,year))
                except:
                    state_trip_data[state][year][month]=""
                

    issues=["NO GPS","Technical","Network","Others"]
    analysis_list=[]
    for state in states:
        data={}
        data["State"]=state
        #data["Network Operator"]=call_df[call_df["Vehicle Number"]==vehicle_no]["Network Operator"].unique()[0]
        #data["company"]=call_df[call_df["Vehicle Number"]==vehicle_no]["Company Name"].unique()[0]
        #data["state office"]=call_df[call_df["Vehicle Number"]==vehicle_no]["State"].unique()[0]

        for year in years:
            data["year"]=year
            yearly_call_data=state_call_data[state][year]
            yearly_trip_data=state_trip_data[state][year]


            for month in months:
                data["month"]=month
                try:
                    monthly_state_call_data=yearly_call_data[month]
                    
                except:
                    monthly_state_call_data={}
                try:
                    monthly_state_trip_data=yearly_trip_data[month]
                except:
                    monthly_state_trip_data={}
                
                data[year+month+" calls"]=len(monthly_state_call_data)
                try:
                    data[year+month+" trips"]=monthly_state_trip_data["Invoice number"].nunique()
                except:
                    data[year+month+" trips"]=0
                try:
                    data[year+month+" trips with calls"]=monthly_state_call_data["Invoice number"].nunique()
                except:
                    data[year+month+" trips with calls"]=0
                try:
                    data[year+month+" locations visited"]=monthly_state_trip_data["Destination"].nunique()
                except:
                    data[month+" locations visited"]=0
                try:
                    data[month+" locations with call"]=monthly_state_call_data["Location name"].nunique()
                except:
                    data[month+" locations with call"]=0
                try:
                    data[year+month+" tt's taken trip"]=monthly_state_trip_data["Vehicle Number"].nunique()
                except:
                    data[year+month+" tt's taken trip"]=0

                try:
                    data[year+month+" tt's with call"]=monthly_state_call_data["Vehicle Number"].nunique()
                except:
                    data[year+month+" tt's with call"]=0

                
                try:
                    problem=monthly_state_call_data["Problem"].value_counts()
                except:
                    problem={}
                for issue in issues:
                    try:
                        data[issue+" "+year+month+" calls"]=problem[issue]
                    except:
                        data[issue+" "+year+month+" calls"]=0

            analysis_list.append(data)
            print(data)
    
    location=os.path.join('output',"state analysis.csv")
    analysis_list=pd.DataFrame([analysis_list])
    analysis_list.to_csv(location)
    return location
        

        
        


