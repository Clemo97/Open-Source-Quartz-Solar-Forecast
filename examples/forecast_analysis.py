import pandas as pd
import matplotlib.pyplot as plt
from quartz_solar_forecast.forecast import run_forecast
from quartz_solar_forecast.pydantic_models import PVSite
from datetime import datetime, timedelta

def main():
    # Make input data
    site = PVSite(latitude=51.75, longitude=-1.25, capacity_kwp=1.25)
 
    # Calculate the start of the previous day
    ts = (datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)    
    nwp_sources = ['icon', 'gfs', 'ukmo']
    
    # Dictionary to store DataFrames
    df_dict = {}
    
    for source in nwp_sources:
        # Run forecast
        predictions_df = run_forecast(site=site, ts=ts, nwp_source=source)
        
        # Store DataFrame in dictionary
        df_dict[source] = predictions_df

    # Plot all data in one image
    plt.figure(figsize=(12, 8))
    
    for source, df in df_dict.items():
        plt.plot(df.index, df['power_kw'], label=f'{source} Forecast')
    
    plt.xlabel('Date and Time')
    plt.ylabel('Power (kW)')
    plt.title('Forecast Comparison')
    plt.ylim(0, 1.0)
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('forecast_comparison.png')
    plt.close()
    print("Combined plot saved as forecast_comparison.png")

if __name__ == "__main__":
    main()
