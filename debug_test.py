from backend.astrology_engine import calculate_chart
import sys

try:
    chart = calculate_chart("Test", "1990-01-01", "12:00", "Chennai")
    print("Success:", chart)
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
