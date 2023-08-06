import datetime

from blend360_all_star_clickstream_api.datafetch import DataFetch

test_scope_name = "all_star_cohort10_project"
test_key_name = "api_key"

datafetcher = DataFetch(test_scope_name, test_key_name)

job_id = datafetcher.fetchData(
    start_date = datetime.date(2022, 2, 1), 
    end_date=  datetime.date(2022, 2, 5),
    destination_bucket = "allstar-training-cowcode",
    destination_directory = "clickstream/testrun1/partition1",
    table_name = "clickstream")

assert isinstance(job_id, str), f"clickstream_api.datafetch.DataFetch.fetchData should return a string value! Returned: {job_id}"

job_status = datafetcher.checkStatus(job_id)
valid_status = ["SUCCEEDED", "FAILED", "RUNNING"]
assert job_status in valid_status, f"clickstream_api.datafetch.DataFetch.checkStatus should return a value in {valid_status} Returned: {job_status}"

print("clickstream_api.datafetch.DataFetch: All Tests Passed!")