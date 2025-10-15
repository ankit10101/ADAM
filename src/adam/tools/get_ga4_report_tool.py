from typing import Optional
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
import pandas as pd
from datetime import datetime
from src.adam.utility_functions import get_gcp_service_account_credentials
from crewai.tools import tool


@tool
def get_a_ga4_report(
    dimensions: list[str],
    metrics: list[str],
    date_ranges: list[tuple[str, str]],
    property_id: str,
    stream_id: str,
    dimension_regex_filters: Optional[dict[str, str]] = dict(),
    sort_by_metrics: Optional[list[str]] = [],
    ascending_bools: Optional[list[bool]] = [],
) -> str:
    """
    Use this tool to get/run a report from/on a GA4 property. It will help you get/run any report from/on any GA4 property. Strictly do not try to interpret the input dates. It doesn't matter if they are from the past or in the future. Simply use the tool with the input dates, get the output, and respond accordingly.

    It takes in the following parameters:
    * dimensions (list[str]): A list of all the report dimensions
    * metrics (list[str]): A list of all the report metrics
    * date_ranges (list[tuple[str, str]]): A list of tuples of length two denoting the different date ranges to compare. The first element of the tuple will be the starting date, and the second element will be the end date. All the date strings should be in the format YYYY-MM-DD.
    * property_id (str): The GA4 property ID to get/run the report from/on
    * stream_id (str): The Stream ID within the GA4 property to get/run the report from/on
    * The following parameters are optional:
        * dimension_regex_filters (dict[str, str]): It is a Python dictionary object representing the applicable regex filters on different dimensions. The dictionary keys will be the various dimensions to apply the regex filter on, and the values will be the corresponding regex filter string. The default value is an empty dictionary.
        * sort_by_metrics (list[str]) and ascending_bools (list[bool]) are also optional parameters. They sort the report by any metric(s) from the `metrics` parameter. The former comprises the names of all the metrics to sort by, and the latter (a list of Python booleans) denotes the sorting order for each metric. Use True to sort the report by a metric in ascending order and False in descending order.

    It returns a string specifying whether the tool ran successfully or encountered an exception. You should stop in either scenario and respond accordingly.

    The report (if fetched/extracted successfully) gets saved in an Excel file. If the report's rows are less than 50, then the output string also comprises the report data (dimensions and metrics values). Otherwise, the report will only be available in the Excel file. You should convey the user accordingly.
    """
    # client = BetaAnalyticsDataClient(credentials = get_gcp_service_account_credentials('../ga4-apis-practice@ga4-apis-practice.json', ['https://www.googleapis.com/auth/analytics.readonly']))
    client = BetaAnalyticsDataClient(
        credentials=get_gcp_service_account_credentials(
            "../kana-automation-account-9a7686dc348d.json",
            ["https://www.googleapis.com/auth/analytics.readonly"],
        )
    )

    dimensions = [Dimension(name=dimension) for dimension in dimensions]
    metrics = [Metric(name=metric) for metric in metrics]
    date_ranges = [
        DateRange(start_date=date_range[0], end_date=date_range[1])
        for date_range in date_ranges
    ]
    filter_expressions = [
        FilterExpression(
            filter=Filter(
                field_name="streamID",
                string_filter=Filter.StringFilter(value=stream_id),
            )
        )
    ]

    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=dimensions,
            metrics=metrics,
            date_ranges=date_ranges,
            dimension_filter=FilterExpression(
                and_group=FilterExpressionList(
                    expressions=filter_expressions
                    + [
                        FilterExpression(
                            filter=Filter(
                                field_name=dimension,
                                string_filter=Filter.StringFilter(
                                    match_type=Filter.StringFilter.MatchType.FULL_REGEXP,
                                    value=dimension_regex_filters[dimension],
                                ),
                            )
                        )
                        for dimension in dimension_regex_filters
                    ]
                )
            ),
            limit=250000,
        )

        response = client.run_report(request)

        data = []
        for row in response.rows:
            _row = []
            for dimension_value in row.dimension_values:
                _row.append(dimension_value.value)
            for metric_value in row.metric_values:
                _row.append(metric_value.value)
            data.append(_row)

        columns = []
        for dimension in response.dimension_headers:
            columns.append(dimension.name)
        for metric in response.metric_headers:
            columns.append(metric.name)

        report = pd.DataFrame(data, columns=columns)
        file_name = f"ga4_reports/{property_id}-{stream_id}_report_{datetime.now().strftime(r'%d-%m-%Y %H-%M-%S')}.xlsx"
        report.to_excel(file_name, index=False)

        if sort_by_metrics:
            report.sort_values(sort_by_metrics, ascending=ascending_bools, inplace=True)

        if len(report) < 50:
            return f"Congratulations! The tool ran successfully.\n\nYou can see the Excel export here: {file_name}\nThe report has less than 50 rows. Here is the report.\n\n{report}\n\nStop here and convey accordingly."
        else:
            return f"Congratulations! The tool ran successfully.\n\nYou can see the Excel export here: {file_name}\nThe report has more than 50 rows. Hence, it is only available in the above Excel file. Stop here and convey accordingly."
    except Exception as e:
        return f"An exception occurred while using the tool!\nHere it is. {e}\n\nStop here and respond with the exception summary."
