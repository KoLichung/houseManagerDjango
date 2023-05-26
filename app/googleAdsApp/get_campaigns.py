#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example illustrates how to get all campaigns.

To add campaigns, run add_campaigns.py.
"""


import argparse
import sys
import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def main(client, customer_id):
    # client 是一個 global client
    # customer_id 是
    print(f'the client {client}')
    print(f'the customer id {customer_id}')

    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""

    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=customer_id, query=query)

    for batch in stream:
        for row in batch.results:
            print(
                f"Campaign with ID {row.campaign.id} and name "
                f'"{row.campaign.name}" was found.'
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    # googleads_client = GoogleAdsClient.load_from_storage(version="v13")
    # 如要指定 google-ads.yaml 檔案的所在位置，您可以在呼叫檔案時將路徑當做字串傳遞給方法：
<<<<<<<< HEAD:app/googleAdsApp/get_campaigns.py
    PWD = os.path.dirname(os.path.realpath(__file__ )) 
    thePath = os.path.join(PWD, "google-ads.yaml")

    # googleads_client = GoogleAdsClient.load_from_storage("/Users/JuneWen/ChiJia/django/houseManagerDjango/google-ads.yaml")

    googleads_client = GoogleAdsClient.load_from_storage(thePath)
========
    googleads_client = GoogleAdsClient.load_from_storage("/Users/JuneWen/ChiJia/django/houseManagerDjango/google_ads/google-ads.yaml")
>>>>>>>> 46c5c62c05395b5848bdbf818abc01849bbbcf9b:google_ads/get_campaigns.py
    

    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)