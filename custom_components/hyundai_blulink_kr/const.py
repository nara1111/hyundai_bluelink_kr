"""Constants for the Hyundai Connect Korea integration."""

DOMAIN: str = "hyundai_connect_korea"

CONF_SCAN_INTERVAL: str = "scan_interval"

CONF_CLIENT_ID: str = "client_id"
CONF_CLIENT_SECRET: str = "client_secret"
CONF_REDIRECT_URI: str = "redirect_uri"

DEFAULT_SCAN_INTERVAL: int = 30

API_BASE_URL: str = "https://prd.kr-ccapi.hyundai.com/api/v1"
API_AUTHORIZE_URL: str = f"{API_BASE_URL}/user/oauth2/authorize"
API_TOKEN_URL: str = f"{API_BASE_URL}/user/oauth2/token"

API_VEHICLE_URL: str = f"{API_BASE_URL}/car/profile/carlist"
API_DTE_URL: str = f"{API_BASE_URL}/car/status/{{carId}}/dte"
API_ODOMETER_URL: str = f"{API_BASE_URL}/car/status/{{carId}}/odometer"
API_EV_BATTERY_URL: str = f"{API_BASE_URL}/car/status/{{carId}}/ev/battery"
API_EV_CHARGING_URL: str = f"{API_BASE_URL}/car/status/{{carId}}/ev/charging"

API_WARNING_FUEL_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/lowFuel"
API_WARNING_TIRE_PRESSURE_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/tirePressure"
API_WARNING_LAMP_WIRE_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/lampWire"
API_WARNING_SMART_KEY_BATTERY_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/smartKeyBattery"
API_WARNING_WASHER_FLUID_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/washerFluid"
API_WARNING_BRAKE_OIL_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/breakOil"
API_WARNING_ENGINE_OIL_URL: str = f"{API_BASE_URL}/car/status/warning/{{carId}}/engineOil"

SENSOR_TYPES: dict[str, tuple[str, str | None]] = {
    "odometer": ("Odometer", "km"),
    "dte": ("Distance to Empty", "km"),
    "ev_battery_level": ("EV Battery Level", "%"),
    "ev_charging_status": ("EV Charging Status", None),
    "ev_remaining_time": ("EV Remaining Charging Time", "min"),
    "fuel_warning": ("Fuel Warning", None),
    "tire_pressure_warning": ("Tire Pressure Warning", None),
    "lamp_wire_warning": ("Lamp Wire Warning", None),
    "smart_key_battery_warning": ("Smart Key Battery Warning", None),
    "washer_fluid_warning": ("Washer Fluid Warning", None),
    "brake_oil_warning": ("Brake Oil Warning", None),
    "engine_oil_warning": ("Engine Oil Warning", None),
}

ERROR_MESSAGES: dict[str, str] = {
    "4002": "Invalid Request Body",
    "4003": "Invalid Request Value",
    "4010": "Require authentication",
    "4011": "Invalid Access Token",
    "4012": "Deactivated User",
    "4045": "No data",
    "5001": "Internal Server Error",
    "9999": "Undefined Error",
}
