# --------------------------------------------------------------------------------------
# Copyright(c) 2023 Joseph Jones,  MIT License @  https://opensource.org/licenses/MIT
# --------------------------------------------------------------------------------------
def report(report, test_result):
    report.add_description(
        """ This test run the trim command to free up unused blocks.  This test is typically run
         at the start of any performance testing to ensure the drive is starting with the most
        blocks free.
        <br/><br/>
        """
    )
    report.add_results(test_result)

    data = test_result["data"]

    if data["return code"] == 0:
        report.add_paragraph(""" The trim command passed. """)
    else:
        report.add_paragraph(f""" The trim command failed with code {data["return code"]}. """)

    report.add_verifications(test_result)
