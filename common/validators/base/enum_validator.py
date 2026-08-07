from common.apiexceptions.base import InvalidChoice

class EnumValidator:

    @staticmethod
    def validate_choice(value, choices, field_name):

        valid_choices = [choice[0] for choice in choices]

        if value not in valid_choices:
            raise InvalidChoice(
                detail={
                    field_name: f"Invalid {field_name}"
                }
            )