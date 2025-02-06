def get_user_input():
    print("\nEnter values for risk prediction:")
    air_quality = float(input("Air Quality Index: "))
    inhaler_usage = float(input("Inhaler Usage Frequency: "))
    motion = float(input("Motion Activity: "))

    return [air_quality, inhaler_usage, motion]
