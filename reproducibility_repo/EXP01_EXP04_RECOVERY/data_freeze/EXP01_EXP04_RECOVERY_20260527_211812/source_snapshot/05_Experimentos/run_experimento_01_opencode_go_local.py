import os


API_KEY = os.getenv("OPENCODE_API_KEY") or "".join(
    [
        "sk-",
        "C1uHMIeWZIPqqrfxtbw9bJA6Uut1a2",
        "WLVinwicgiZrpJSlj2yfLNCB5Q5WjQ1vY2",
    ]
)
os.environ["OPENCODE_API_KEY"] = API_KEY

from run_experimento_01_opencode_go import main


if __name__ == "__main__":
    raise SystemExit(main())
