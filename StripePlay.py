import stripe

stripe.api_key = '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'

def charge_credit_card(amount, currency, card_number, exp_month, exp_year, cvc):
    try:
        print("Creating a token...")
        # Create a new Stripe token
        token = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )
        print(f"Token created: {token.id}")
        
        print("Creating a charge...")
        # Charge the card
        charge = stripe.Charge.create(
            amount=amount,  # Amount in cents
            currency=currency,
            source=token.id,
            description="Charge for product/service",
        )
        
        print("Charge successful!")
        return charge
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err  = body.get('error', {})
        print(f"Status is: {e.http_status}")
        print(f"Type is: {err.get('type')}")
        print(f"Code is: {err.get('code')}")
        print(f"Message is: {err.get('message')}")
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        print("Rate limit error:", e)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print("Invalid parameters:", e)
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print("Authentication error:", e)
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print("Network error:", e)
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print("Stripe error:", e)
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print("An error occurred:", e)

# Example usage
charge = charge_credit_card(
    amount=5000,  # Amount in cents ($50.00)
    currency='usd',
    card_number='4242424242424242',
    exp_month=12,
    exp_year=2024,
    cvc='123'
)

print(charge)

# # Example usage
# charge = charge_credit_card(
#     amount=100,  # Amount in cents ($50.00)
#     currency='usd',
#     card_number='4712134050236668',
#     exp_month=1,
#     exp_year=2026,
#     cvc='134'
# )

# print(charge)
