# Dexcom API Wrapper
[Dexcom](https://www.dexcom.com/) has recently released a new [API](https://developer.dexcom.com/) that enables developers to use data from their glucose sensors to create innovative apps. To get you started, here is a wrapper meant to be a starting template for your app. &emsp;
https://developer.dexcom.com/
<br>

## Features
This wrapper takes care of authentication, requests, and fetching data from the 5 `GET` [endpoints available](https://developer.dexcom.com/endpoint-overview):
- [`calibrations`](https://developer.dexcom.com/get-calibrations): user's calibration events.
- [`dataRange`](https://developer.dexcom.com/get-datarange): user's earliest and latest times for calibration, estimated glucose value (EGV), and event records. Useful for providing start and end dates for the other endpoints.
- [`devices`](https://developer.dexcom.com/get-devices): user's device information, including G4, G5, and G6 standalone receivers, the G5 and G6 mobile apps, and transmitters.
- [`egvs`](https://developer.dexcom.com/get-egvs): user's estimated glucose values (EGVs), including trend and status information.
- [`events`](https://developer.dexcom.com/get-events): user's event records. This includes carbohydrate intake, insulin doses, exercise, and health events that are entered in the receiver interface or through the mobile app.
<br><br>


## Setup
1. Make a [Dexcom Developer](https://developer.dexcom.com/) account.
2. Create an app on Dexcom Developer to get `CLIENT_ID` and `CLIENT_SECRET`.
    1. Go to https://developer.dexcom.com/user/me/apps
    2. Click "Add an App ⊕"
    3. Name it whatever you like and click "Create"
    4. In the "Redirect URI" field, write `https://localhost:8080`and click "Save"\
    (unless you'd like to use something else in particular)
    5. Under "Authentication", copy the `CLIENT_ID` and `CLIENT_SECRET`.
3. Install `rauth`.\
    `pip install rauth`\
    OR\
    `pip install -r requirements.txt`
4. Enter `CLIENT_ID` and `CLIENT_SECRET` on lines `11` and `12` respectively of `app.py`.\
    **NOTE**: If you entered a different "Redirect URI" than `https://localhost:8080` on step 2.iv, then change line `16`.
5. Run application to generate tokens.
    1. Run `python dexcom.py`
    2. Open the URL that's printed in the console. Sign in to your Dexcom Account.\
        If you don't have a Dexcom account, refer to [Using Sandbox Data](#using-sandbox-data) and repeat step 5.
    3. Authorize the application to view your data. Check "Share Data", sign and click "Save and Continue".
    4. Copy the redirected URL and paste it into the console.\
        It will look something like `https://localhost:8080/?code=13d9f01422495234231233bfdb123351e0f`.
    5. EGVs should be printed to your console!
<br><br>


## Usage
Other than for setup and reference purposes, you don't need to access `api.py`. Your application implementation will be done entirely in `dexcom.py`. To use the API, use the `dexcomAPI` function.

`dexcomAPI` takes three arguments:
- `endpoint`: The endpoint to use: `calibrations`, `dataRange`, `devices`, `egvs`, or `events`. All endpoints besides `dataRange` require a time window indicated by the `start` and `end` parameters below.\
    Default: `egvs`. 
- `start`: the beginning date of the time window. Use `dataRange` endpoint to get the earliest time.\
    Default: `2022-02-27T00:30:00`.
- `end`: the ending date of the time window. Use `dataRange` endpoint to get the latest time.\
    Default: `2022-02-27T02:35:00`.
<br><br>

`dexcomAPI` returns a JSON object. Refer to the [Features](#features) section for each endpoint details. 


## Using Sandbox Data
Dexcom has provided a sandbox environment containing simulated CGM data is available for all Registered Developers to test their applications. The data in the sandbox emulates real Dexcom data, and all of the [endpoints](https://developer.dexcom.com/endpoint-overview) available in the production environment are also available in the sandbox environment.

To use the Sandbox data, comment out line `10` and uncomment line `9`. This makes the endpoints use the base URL of `https://sandbox-api.dexcom.com/v2/` instead of `https://api.dexcom.com/v2/`.

During authentication, you will be asked to select a Sandbox user. Refer to the Users section of [Dexcom Developer Docs](https://developer.dexcom.com/sandbox-data) to select data that works best for your application. Once you've chosen, type your (or any) name to authorize.
<br><br>


## Limitations
- According to [Dexcom Developer FAQs](https://developer.dexcom.com/content/frequently-asked-questions), the Dexcom API does **NOT** provide real-time estimated glucose values. All values reported by the `/egvs` endpoint are intentionally delayed by 3 hours. If you'd like real-time values, I highly **recommend** checking out [Nightscout](https://github.com/nightscout/cgm-remote-monitor).
- This wrapper does NOT deal with the [`/statistics`](https://developer.dexcom.com/post-statistics) endpoint. You can find more information about endpoints on [Dexcom Developer Docs](https://developer.dexcom.com/endpoint-overview).
- This application is simply a wrapper. It does not manipulate or analyze the Dexcom API data in any way. That is left up to you. I got bulk of the work out of the way so read up on [Dexcom Developer Docs](https://developer.dexcom.com/overview) and change this application to your liking. All the best!
<br><br>


## License
See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
<br><br>

<p align="center">
Donate, buy me a <a href="https://buymeacoff.ee/PrinceSingh" target="_blank">Pizza</a> or <a href="https://paypal.me/PrinceSingh25" target="_blank">PayPal</a> me if you'd like to see this project expanded and support me. :) <br> <br>
<a href="https://www.paypal.com/donate?business=3Y9NEYR4TURT8&item_name=Making+software+and+hacking+the+world%21+%E2%99%A5&currency_code=USD" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" alt="Paypal me" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a> <br> <br>
<a href="https://www.buymeacoffee.com/PrinceSingh" target="_blank"><img src="https://i.imgur.com/H7BJq0V.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
<a href="https://www.paypal.me/PrinceSingh25" target="_blank"><img src="https://i.imgur.com/FDuYJBd.png" alt="Paypal me" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>
