from ninebit_ciq import NineBitCIQClient
import time

try:
    client = NineBitCIQClient(
        api_key="a3a2c7ba-6937-4796-afc8-42d54ef3074f",
        # base_url="http://localhost:8090"
    )

    def on_done(error, data):
        if error:
            print(f"Ingest_file failed: {error}")
        else:
            print(f"Ingest_file succeeded: {str(data)}")

    client.ingest_file(file="files/geo_chap_8.pdf", callback=on_done)

    # query = "What are the factors that control temperature distribution on the surface of the earth?"
    query = "What are land breeze?"
    response = client.rag_query(query=query)
    print(f"Query response is {response}")

except Exception as ex:
    print(f"Error: {str(ex)}")