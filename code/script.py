import pandas as pd
import numpy as np

def covid_vaccine(vaccination_status_files, user_meta_file, output_file):
    """This function takes  vaccination_status_files and user_meta_file paths
    using this all the covid vaccination numbers needs to be stored in the given output file as TSV
    Args:
        vaccination_status_files: A List containing file path to the TSV vaccination_status_file.
        user_meta_file: A file path to TSV file containing User information.
        output_file: File path where output TSV results are should be stored, 
    Returns:
      None (doesnt return anything)
    """
    
    #Reading the input files as pandas dataframe

    df_vs = pd.DataFrame(columns = ["user", "vaccine", "date"])
    for vs_file in vaccination_status_files:
        new_df = pd.read_csv(vs_file, sep="\t")

        df_vs = df_vs.append(new_df, ignore_index = True)


    # Validation of input

    # Vaccine is of type string, valid vaccine's are A,B and C, anything other are invalid.
    valid_vaccines = ["A", "B", "C"]
    df_vs = df_vs[df_vs["vaccine"].isin(valid_vaccines)]


    # Date is of type date in dd-mm-yyyy format, it should be between 1st February 2020 to 30th November 2021 (Inclusive).
    start_date = "2020-02-01"
    end_date = "2021-11-30"
    date_sr = pd.Series(pd.date_range(start_date, end_date, freq='d'))
    valid_dates = date_sr.dt.strftime('%d-%m-%Y')
    

    # Final vaccination_status_files dataframe
    df_vs = df_vs[df_vs.date.isin(valid_dates)]

    # Final user_meta_file dataframe
    df_md = pd.read_csv(user_meta_file, sep="\t")


    # Merge the dataframes based on "user" column
    df_merged = df_vs.join(df_md.set_index('user'), on='user')


    # Get the number of users vaccinated by city, state, vaccine or gender
    final_df = df_merged.groupby(["city", "state", "vaccine", "gender"])["user"].nunique().reset_index(name='unique_vaccinated_people')
    final_df = final_df.sort_values(by=["city", "state", "vaccine", "gender"]) 
    

    # Save the results to the output_file as TSV
    final_df.to_csv(output_file, sep="\t", index=False)
    
    pass