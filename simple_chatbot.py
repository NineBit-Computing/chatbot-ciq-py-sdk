from ninebit_ciq import NineBitCIQClient
import time

try:
    client = NineBitCIQClient(
        # api_key="4a4e88b4-88cb-4d66-aefb-c4dcee991cff",
        api_key="ad413818-5d0e-4eb3-ab7d-230d0009e170",
        base_url="http://localhost:8090"
    )

    dt = client.get_design_time_workflow()

    def on_done(error):
        if error:
            print(f"Task failed: {error}")
        else:
            print("Task succeeded")

    client.ingest_file(file="files/geo_chap_9.pdf", callback=on_done)

except Exception as ex:
    print(f"Error: {str(ex)}")