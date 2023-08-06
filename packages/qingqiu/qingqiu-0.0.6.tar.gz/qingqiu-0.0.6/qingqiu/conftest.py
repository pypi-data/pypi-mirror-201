import pytest
from py._xmlgen import html





@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    try:
        report = outcome.get_result()
        report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")  # 解决乱码
        report.description = str(item.function.__doc__)
    except:
        pass
        

def pytest_html_report_title(report):
    report.title="测试报告"

def pytest_configure(config):
    config._metadata.pop("JAVA_HOME")


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    try:
        cells.pop(-1)  # 删除link列
        cells.insert(1, html.th('Description'))
    except:
        pass
    


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    try:
        cells.pop(-1)  # 删除link列
        cells.insert(1, html.td(report.description))
        
    except:
        pass

