Xunit parser
============

.. image:: https://travis-ci.org/UkuLoskit/xunit.svg?branch=master
    :target: https://travis-ci.org/UkuLoskit/xunit

Xunit Parser provides a common Python interface for different formats of Xunit XML.

Usage
-----

Regardless of whether there are multiple test suites, the library always wraps the results in a TestSuites object

    >>> test_suites = XunitParser().parse('my.xml')
    >>> for test_suite in test_suites.test_suites:
            for test_case in test_suite.test_cases:
                print(test_case)


Xunit Parser can also be used in situations where XML from unstrusted sources must be safely processed.

For example, you can use Xunit Parser in conjunction with the excellent `defusedxml` library: 

    >>> import defusedxml
    >>> test_suites = XunitParser(elementree_class=defusedxml.ElementTree).parse('my.xml')
