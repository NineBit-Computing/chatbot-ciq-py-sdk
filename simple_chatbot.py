from ninebit_ciq import NineBitCIQClient

try:
    client = NineBitCIQClient(
        # api_key="4a4e88b4-88cb-4d66-aefb-c4dcee991cff",
        api_key="c4ccc51e-3654-4719-aeb1-7caf9c0c25d4",
        base_url="http://localhost:8090"
    )

    dt = client.get_design_time_workflow()

    client.ingest_file(file="files/geo_chap_9.pdf")
    # print("Success File Upload")
    # print(f"Success: {dt}")

except Exception as ex:
    print(f"Error: {str(ex)}")