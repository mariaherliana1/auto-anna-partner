from src.FileConfig import Files
from dataclasses import dataclass

CONFIG: CONFIG = [
    # Add your file paths here.
    Files(
        client="bullishfx-id enduser", # 10/sec
        dashboard="202504/DB/bullishfx-id enduser.csv",
        console="202504/console/bullishfx-id enduser.csv",
        output="202504/merge/bullishfx-id enduser.csv",
    ),
    Files(
        client="bullishfx-id invoice", # 9.5/sec
        dashboard="202504/DB/bullishfx-id invoice.csv",
        console="202504/console/bullishfx-id invoice.csv",
        output="202504/merge/bullishfx-id invoice.csv",
    ),
    Files(
        client="threetigerinc-id enduser", # 13
        dashboard="202504/DB/threetigerinc-id enduser.csv",
        console="202504/console/threetigerinc-id enduser.csv",
        output="202504/merge/threetigerinc-id enduser.csv",
    ),
    Files(
        client="threetigerinc-id invoice", # 12
        dashboard="202504/DB/threetigerinc-id invoice.csv",
        console="202504/console/threetigerinc-id invoice.csv",
        output="202504/merge/threetigerinc-id invoice.csv",
    ),
    Files(
        client="sinarpagi-id enduser", #780
        dashboard="202504/DB/sinarpagi-id enduser.csv",
        console="202504/console/sinarpagi-id enduser.csv",
        output="202504/merge/sinarpagi-id enduser.csv",
    ),
    Files(
        client="sinarpagi-id invoice", #720
        dashboard="202504/DB/sinarpagi-id invoice.csv",
        console="202504/console/sinarpagi-id invoice.csv",
        output="202504/merge/sinarpagi-id invoice.csv",
    ),
    Files(
        client="micehub-id enduser", #780
        dashboard="202504/DB/micehub-id enduser.csv",
        console="202504/console/micehub-id enduser.csv",
        output="202504/merge/micehub-id enduser.csv",
    ),
    Files(
        client="micehub-id invoice", #720
        dashboard="202504/DB/micehub-id invoice.csv",
        console="202504/console/micehub-id invoice.csv",
        output="202504/merge/micehub-id invoice.csv",
    ),
    Files(
        client="kozystay-id enduser", #780
        dashboard="202504/DB/kozystay-id enduser.csv",
        console="202504/console/kozystay-id enduser.csv",
        output="202504/merge/kozystay-id enduser.csv",
    ),
    Files(
        client="kozystay-id invoice", #720
        dashboard="202504/DB/kozystay-id invoice.csv",
        console="202504/console/kozystay-id invoice.csv",
        output="202504/merge/kozystay-id invoice.csv",
    ),
    Files(
        client="siemens-id enduser", #1700, 780
        dashboard="202504/DB/siemens-id enduser.csv",
        console="202504/console/siemens-id enduser.csv",
        output="202504/merge/siemens-id enduser.csv",
    ),
    Files(
        client="siemens-id invoice", #1500, 720
        dashboard="202504/DB/siemens-id invoice.csv",
        console="202504/console/siemens-id invoice.csv",
        output="202504/merge/siemens-id invoice.csv",
    ),
    Files(
        client="gaji-id end-user", #799
        dashboard="202504/DB/gaji-id enduser.csv",
        console="202504/console/gaji-id enduser.csv",
        output="202504/merge/gaji-id enduser.csv",
    ),
    Files(
        client="gaji-id invoice", #720
        dashboard="202504/DB/gaji-id invoice.csv",
        console="202504/console/gaji-id invoice.csv",
        output="202504/merge/gaji-id invoice.csv",
    ),

]