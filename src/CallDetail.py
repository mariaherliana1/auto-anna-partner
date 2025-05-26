from src.utils import parse_phone_number, parse_iso_datetime, parse_time_duration, parse_call_memo, classify_number
from src.idn_area_codes import EMERGENCY_NUMBERS, INTERNATIONAL_PHONE_PREFIXES
import math
from src.utils import call_hash, classify_number, format_datetime_as_human_readable, format_timedelta, format_username, parse_call_memo, parse_iso_datetime, parse_phone_number
from config import CONFIG
from src.international_rates import INTERNATIONAL_RATES

class CallDetail:
    def __init__(
        self,
        client: str,
        sequence_id: str,
        user_name: str,
        call_from: str,
        call_to: str,
        call_type: str,
        dial_start_at: str,
        dial_answered_at: str,
        dial_end_at: str,
        ringing_time: str,
        call_duration: str,
        call_memo: str,
        call_charge: str,
        file_name: str,
    ):
        self.client = client
        self.sequence_id = sequence_id
        self.user_name = user_name
        self.call_from = parse_phone_number(call_from)  # Normalizing here
        self.call_to = parse_phone_number(call_to)      # Normalizing here
        self.call_type = call_type
        self.dial_start_at = parse_iso_datetime(dial_start_at)
        self.dial_answered_at = (
            parse_iso_datetime(dial_answered_at) if dial_answered_at != "-" else None
        )
        self.dial_end_at = parse_iso_datetime(dial_end_at)
        self.ringing_time = parse_time_duration(ringing_time)
        self.call_duration = parse_time_duration(call_duration)
        self.call_memo = parse_call_memo(call_memo)
        self.file_name = file_name
        self.number_type = classify_number(self.call_to, self.call_type, self.call_from, self.call_to)
        self.call_charge = self.calculate_call_charge()

    def calculate_per_minute_charge(self, rate: float) -> str:
        minutes = math.ceil(self.call_duration.total_seconds() / 60)
        return str(minutes * rate)

    def calculate_per_second_charge(self, rate: float) -> str:
        return str(self.call_duration.total_seconds() * rate)

    @property
    def matched_client(self):
        if not hasattr(self, "_matched_client"):
            self._matched_client = next(
                (config_entry for config_entry in CONFIG if config_entry.client == self.client),
                None
            )
        return self._matched_client

    @property
    def is_enduser(self):
        return self.matched_client is not None and "enduser" in self.client

    SPECIAL_ZERO_CHARGE_CALLERS = {"2150913403", "85161662298", "85157455618", "82248400487", "2150913400", "2131141271"}    

    def calculate_call_charge(self) -> str:
        number_type = classify_number(self.call_to, self.call_type, self.call_from, self.call_to)

        # Early skip for non-billable calls, with exception for special incoming number
        if self.call_type in ["Internal Call", "Internal Call (No answer)", "Monitoring", "Answering machine"]:
            return "0"

        if str(self.call_from) in SPECIAL_ZERO_CHARGE_CALLERS:
            return "0"

        if self.call_type == "Incoming call":
            # Special handling for number 2150981440
            if str(self.call_to) == "2150981440":
                rate = 1500 + (200 if self.is_enduser else 0)
                return self.calculate_per_minute_charge(rate)
            return "0"

        if number_type == "Internal Call":
            return "0"

        # Premium or emergency
        if number_type in ["Premium Call", "Toll-Free", "Split Charge"] or number_type in EMERGENCY_NUMBERS.values():
            rate = 1700 + (200 if self.is_enduser else 0)
            return self.calculate_per_minute_charge(rate)

        # International call tiers
        if number_type in INTERNATIONAL_RATES:
            base_rate = INTERNATIONAL_RATES[number_type]
            if self.is_enduser:
                base_rate += 200
            return self.calculate_per_minute_charge(base_rate)

        # Step 2: If not premium/international, check for matched client
        if self.matched_client and self.call_type in {"Outbound call", "Predictive dialer"}:

            # Per-second clients
            client_per_second_rates = {
                "bullishfx-id enduser": 10,
                "bullishfx-id invoice": 9.5,
                "threetigerinc-id enduser": 13,
                "threetigerinc-id invoice": 12,
            }

            if self.client in client_per_second_rates:
                return self.calculate_per_second_charge(client_per_second_rates[self.client])

            # Per-minute clients
            client_per_minute_rates = {
                "sinarpagi-id enduser": 780,
                "sinarpagi-id invoice": 720,
                "julo-id enduser": 780,
                "julo-id invoice": 720,
                "kozystay-id enduser": 780,
                "kozystay-id invoice": 720,
                "micehub-id enduser": 780,
                "micehub-id invoice": 720,
                "siemens-id enduser": 780,
                "siemens-id invoice": 720,
                "gaji-id end-user": 799,
                "gaji-id invoice": 720,
            }

            if self.client in client_per_minute_rates:
                return self.calculate_per_minute_charge(client_per_minute_rates[self.client])

        # Step 3: Default rate (non-special, unmatched client)
        return self.calculate_per_minute_charge(720)

    def to_dict(self) -> dict:
        return {
            "Sequence ID": self.sequence_id,
            "User name": format_username(self.user_name),
            "Call from": self.call_from,
            "Call to": self.call_to,
            "Call type": self.call_type,
            "Number type": classify_number(self.call_to, self.call_type, self.call_from, self.call_to),
            "Dial starts at": format_datetime_as_human_readable(self.dial_start_at),
            "Dial answered at": format_datetime_as_human_readable(
                self.dial_answered_at
            ),
            "Dial ends at": format_datetime_as_human_readable(self.dial_end_at),
            "Ringing time": format_timedelta(self.ringing_time),
            "Call duration": format_timedelta(self.call_duration),
            "Call memo": self.call_memo,
            "Call charge": self.call_charge,
        }

    def hash_key(self) -> str:
        return call_hash(self.call_from, self.call_to, self.dial_start_at)