# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import ee

GEE_KEY_FILE = r"D:\tott\Documents\Work_Projects\json_permission_files\clim-engine-c9bac9f93a65.json"

def main():
    # Initilize ee using
    # ee.Initialize(ee.ServiceAccountCredentials('', key_file=GEE_KEY_FILE))
    ee.Initialize()
    # Import today's cfsv2 image
    cfsv2 = ee.ImageCollection("projects/climate-engine/cfsv2/forecast/eto").first()
    date_val = cfsv2.date().format("YYYYMMdd").getInfo()
    print(date_val)

    # Calulate the mean and median fo the values
    cfsv2_mean = ee.Image(cfsv2.reduce(ee.Reducer.mean()).copyProperties(cfsv2, ["system:time_start"]))
    cfsv2_median = ee.Image(cfsv2.reduce(ee.Reducer.median()).copyProperties(cfsv2, ["system:time_start"]))

    out_img = cfsv2_mean.addBands(cfsv2_median)

    # Export image to asset
    task = ee.batch.Export.image.toAsset(image=out_img,
                                         description=f"Import of: {date_val}",
                                         assetId=f"projects/climate-engine/cfsv2/daily_stash/{date_val}",
                                         maxPixels=1e9
                                         )
    task.start()
    print(task)

if __name__ == '__main__':
    print("start")
    main()
