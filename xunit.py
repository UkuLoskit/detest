import datetime
import math
import xml.etree.ElementTree as ET


class XunitParserException(Exception):
    pass


class XMLElementMixin(object):
    def __init__(self, xml_element):
        self._xml_element = xml_element


class TimeMixin(object):
    def _parse_time(self, xml_time_value):
        if xml_time_value is None:
            return None

        if "," in xml_time_value and "." in xml_time_value:
            xml_time_value = xml_time_value.replace(",", "")
        elif "," in xml_time_value and "." not in xml_time_value:
            xml_time_value = xml_time_value.replace(",", ".")

        seconds = float(xml_time_value)
        if math.isnan(seconds):
            return None

        return datetime.timedelta(seconds=seconds)


class TestSuiteCommonMixin(TimeMixin):

    @property
    def name(self):
        return self._xml_element.get('name') if self._xml_element is not None else None

    @property
    def tests(self):
        return int(self._xml_element.get('tests')) if self._xml_element is not None else None

    @property
    def skipped(self):
        return int(self._xml_element.get('skip', 0)) if self._xml_element is not None else None

    @property
    def failures(self):
        return int(self._xml_element.attrib.get('failures', 0)) if self._xml_element is not None else None

    @property
    def errors(self):
        return int(self._xml_element.attrib.get('errors', 0)) if self._xml_element is not None else None

    @property
    def time(self):
        return self._parse_time(self._xml_element.attrib.get('time')) if self._xml_element is not None else None


class TestSuites(XMLElementMixin, TestSuiteCommonMixin):
    ROOT_TAG = "testsuites"

    def __init__(self, xml_element=None):
        super(TestSuites, self).__init__(xml_element)
        self.test_suites = [TestSuite(el) for el in xml_element.findall(TestSuite.ROOT_TAG)] if xml_element is not None else []

    def __str__(self):
        return "\n".join([str(suite) for suite in self.test_suites])


class TestSuite(XMLElementMixin, TestSuiteCommonMixin):
    ROOT_TAG = "testsuite"

    def __init__(self, xml_element):
        super(TestSuite, self).__init__(xml_element)
        self.timestamp = xml_element.attrib.get('timestamp', 0.0)
        self.test_cases = [
            TestCase(el) for el in xml_element.findall(TestCase.ROOT_TAG)
        ]
        self.properties = self._parse_properties()

    def _parse_properties(self):
        properties = self._xml_element.find("properties")
        if properties is None:
            return {}

        return {element.attrib['name']: element.attrib["value"] for element in properties.findall("property") if element.attrib}

    def __str__(self):
        return "Test suite: %s\n" % self.name +\
            "tests: %s\n" % self.tests+\
            "failures: %s\n" % self.failures+\
            "skipped: %s\n" % self.skipped+\
            "timestamp: %s\n" % self.timestamp+\
            "duration: %ss" % self.time


class TestCase(TimeMixin):
    ROOT_TAG = "testcase"

    def __init__(self, xml_element):

        self.name = xml_element.attrib.get("name")
        self.class_name = xml_element.attrib.get("classname")
        self.time = self._parse_time(xml_element.attrib.get("time"))
        failure, error = xml_element.find("failure"), xml_element.find('error')
        self.failure = Failure(failure)  if failure is not None else None
        self.error = Error(error) if error is not None else None
        self.error = Error(error) if error is not None else None
        std_out, std_err = xml_element.find("system-out"), xml_element.find("system-err")
        self.stdout = std_out.text if std_out is not None else None
        self.stderr = std_err.text if std_err is not None else None

    def __str__(self):
        return "class: %s, time: %s" % (self.class_name, self.time)


class Fault(object):
    def __init__(self, xml_element):
        self.type = xml_element.attrib.get('type')
        self.message = xml_element.attrib.get('message')
        self.content = xml_element.text

    def __str__(self):
        return "type: %s, message: %s, text: %s" % (self.type, self.message, self.content)


class Failure(Fault):
    pass

class Error(Fault):
    pass


class XunitParser(object):
    def __init__(self, elementree_class=ET):
        self.elementree_class = elementree_class
        self.tree, self.root = None, None

    def parse(self, filename):
        self.tree = self.elementree_class.parse(filename)
        self.root = self.tree.getroot()

        if self.root.tag == TestSuites.ROOT_TAG:
            return TestSuites(self.root)
        elif self.root.tag == TestSuite.ROOT_TAG:
            test_suites = TestSuites()
            test_suites.test_suites = [TestSuite(self.root)]
            return test_suites
        else:
            raise XunitParserException('Unknown XML root tag %s' % self.root.tag)
