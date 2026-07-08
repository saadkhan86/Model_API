import phonenumbers
from phonenumbers import NumberParseException
from app.error_handler.custom_exception import CustomException
def is_valid_phone(phone_str: str, default_region: str = "PK") -> bool:
    try:
        if phone_str.startswith("+"):
            parsed_number = phonenumbers.parse(phone_str, None)
        else:
            parsed_number = phonenumbers.parse(phone_str, default_region)
            
        return phonenumbers.is_valid_number(parsed_number)
    
    except NumberParseException:
        return False

def get_normalized_number(phone_str: str, region: str = "PK") -> str:
    try:
        region_hint = None if phone_str.startswith("+") else region
        parsed = phonenumbers.parse(phone_str, region_hint)
        
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(
                parsed, 
                phonenumbers.PhoneNumberFormat.E164
            )
    except NumberParseException:
        pass 
        
    raise CustomException("phone number is not a valid",400)
