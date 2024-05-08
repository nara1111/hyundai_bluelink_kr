[//]: # ([![hacs_badge]&#40;https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge&#41;]&#40;https://github.com/hacs/integration&#41;)

## 소개 ##

[Hyundai-Kia-Connect/kia_uvo](https://github.com/Hyundai-Kia-Connect/kia_uvo) 프로젝트를 기반으로 한국의 현대 블루링크 API에 맞추어 변경하는 프로젝트. 한국의 경우, 외국과 달리 현대차그룹에서 CCS(Connected Car Service) 관련한 명확한 사업화 전략을 가지고 있어 앞으로도 커뮤니티 기반 CCS 통합구성요소가 나오긴 어려울 것으로 보인다.

본 프로젝트도 개인 개발자 대상으로 현대차그룹에서 API를 테스트 용도로 열어주고 있는 점을 이용하여, 보유하고 있는 개인 차량을 이용하는 수준에서 머무를 수 밖에 없을듯.

[//]: # ()
[//]: # (## Code Maintainers Wanted ##)

[//]: # ()
[//]: # (I no longer have a Kia or Hyundai so don't maintain this like I used to.  Others who are interested in jumping in are welcome to join the project!   Even just pull requests are appreciated! )

[//]: # ()
[//]: # ()
[//]: # (I have baked a custom integration for Kia Uvo / Hyundai Bluelink, this will be working for new account types. Thanks for your hard work [@wcomartin]&#40;https://github.com/wcomartin/kiauvo&#41;. This project was mostly inspired by his [home assistant integration]&#40;https://github.com/wcomartin/kia_uvo&#41;.  This now uses our underlying python package: https://github.com/Hyundai-Kia-Connect/hyundai_kia_connect_api. )

[//]: # ()
[//]: # (## Installation ##)

[//]: # (You can install this either manually copying files or using HACS. Configuration can be done on UI, you need to enter your username and password, &#40;I know, translations are missing, a PR for this would be great!&#41;. )

[//]: # (- AU, EU, CA and US is supported by this.  USA and China support is limited.)

[//]: # (- Genesis Support hasn't been tested and has just been added for Canada only.  Feedback would be appreciated! )

[//]: # (- Multiple cars and accounts are supported. To add additional accounts just go through setup a second time. )

[//]: # (- update - It will fetch the cached information every 30 minutes from Kia Uvo / Hyundai Bluelink Servers. **Now Configurable**)

[//]: # (- force update - It will ask your car for the latest data every 4 hours. **Now Configurable**)

[//]: # (- It will not force update between 10PM to 6AM. I am trying to be cautios here. **Now Configurable**)

[//]: # (- By default, distance unit is based on HA metric/imperial preference, you need to configure each entity if you would like other units.)

[//]: # ()
[//]: # (## Supported entities ##)

[//]: # (- Air Conditioner Status, Defroster Status, Set Temperature)

[//]: # (- Heated Rear Window, Heated Steering Wheel)

[//]: # (- Car Battery Level &#40;12v&#41;, EV Battery Level, Remaining Time to Full Charge)

[//]: # (- Tire Pressure Warnings &#40;individual and all&#41;)

[//]: # (- Charge Status and Plugged In Status)

[//]: # (- Low Fuel Light Status &#40;for PHEV and IC&#41;)

[//]: # (- Doors, Trunk, Window and Hood Open/Close Status)

[//]: # (- Locking and Unlocking)

[//]: # (- Engine Status)

[//]: # (- Location/Coordinates &#40;over GPS&#41; and Geocoded Location using OpenStreetMap &#40;optional, disabled by default&#41;)

[//]: # (- Last Service and Next Service in Canada)

[//]: # (- Odometer, EV Range &#40;for PHEV and EV&#41;, Fuel Range &#40;for PHEV and IC&#41;, Total Range &#40;for PHEV and EV&#41;)

[//]: # (- Latest Update)

[//]: # (- cache update interval, force update interval, blackout start and finish hours)

[//]: # ()
[//]: # (## Supported services ##)

[//]: # (These can be access by going to the developer menu followed by services. )

[//]: # ()
[//]: # (- update: get latest **cached** vehicle data)

[//]: # (- force_update: this will make a call to your vehicle to get its latest data, do not overuse this!)

[//]: # (- start_climate / stop_climate: Starts the ICE engine in some regions or starts EV climate. )

[//]: # (- start_charge / stop_charge: You can control your charging using these services)

[//]: # (- set_charge_limits: You can control your charging capacity limits using this services )

[//]: # (- open_charge_port / close_charge_port:  Open or close the charge port.)

[//]: # ()
[//]: # (| Service                                                    | EU | EU&#40;>2023&#41;  | CA | USA Kia | USA Hyundai | USA Genesis | China |)

[//]: # (|------------------------------------------------------------|----|------------|----|---------|-------------|-------------|-------|)

[//]: # (| Update                                                     | ✔  | ✔          | ✔  | ✔       | ✔           | ✔           | ✔     |)

[//]: # (| Force Update                                               | ✔  | not tested | ✔  | ✔       |             |             | ✔     |)

[//]: # (| Lock Unlock                                                | ✔  | ✖          | ✔  | ✔       | ✔           | ✔           | ✔     |)

[//]: # (| start stop climate                                         | ✔  | ✖          | ✔  | ✔       | ✔           |             | ✔     |)

[//]: # (| start stop charge                                          | ✔  | ✖          | ✔  | ✔       | ✔  |             |       |)

[//]: # (| set charge limits                                          | ✔  | not tested | ✔  | ✔       | ✔  |             |       |)

[//]: # (| open and close charge port&#40;None functional, needs testing&#41; | ✖  | ✖          | ✖  | ✖       | ✖           | ✖           | ✖     |)

[//]: # ()
[//]: # ()
[//]: # (I have posted an example screenshot from my own car.)

[//]: # ()
[//]: # (![Device Details]&#40;https://github.com/Hyundai-Kia-Connect/kia_uvo/blob/master/Device%20Details.PNG?raw=true&#41;)

[//]: # (![Configuration]&#40;https://github.com/Hyundai-Kia-Connect/kia_uvo/blob/master/Configuration.PNG?raw=true&#41;)

[//]: # ()
[//]: # (## Troubleshooting ##)

[//]: # (If you receive an error while trying to login, please go through these steps;)

[//]: # (1. As of now, integration only supports USA, EU and CAD region, so if you are outside, you are more than welcome to create an issue and become a test user for changes to expand coverage. USA coverage isn't complete. )

[//]: # (2. If you are in EU, please log out from UVO app and login again. While logging in, if your account was created in legacy UVO servers, they will be migrated to new Kia Uvo / Hyundai Bluelink servers. Related Issue: https://github.com/Hyundai-Kia-Connect/kia_uvo/issues/22)

[//]: # (3. If you have migrated recently, you might need to wait one day to try again. Related Issue: https://community.home-assistant.io/t/kia-uvo-integration-pre-alpha/297927/12?u=fuatakgun)

[//]: # (4. As a last resort, please double check your account credentials or you can create a new account and share your car from main account to new account.)

[//]: # (5. You can enable logging for this integration specifically and share your logs, so I can have a deep dive investigation. To enable logging, update your `configuration.yaml` like this, we can get more information in Configuration -> Logs page)

[//]: # (```)

[//]: # (logger:)

[//]: # (  default: warning)

[//]: # (  logs:)

[//]: # (    custom_components.kia_uvo: debug)

[//]: # (    hyundai_kia_connect_api: debug)

[//]: # (```)

