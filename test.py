import traceback
import main

try:
    print(main.run_agent('lion'))
except Exception as e:
    print("ERROR CAUGHT IN TEST")
    traceback.print_exc()
