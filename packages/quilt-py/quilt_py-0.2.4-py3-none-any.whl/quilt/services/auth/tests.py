from quilt.services.auth.logic import bearer_token_from_phone_number


def main() -> bytes:
    bearer = bearer_token_from_phone_number(phone_number="+16666666666")
    return bearer


if __name__ == "__main__":
    print(main())
