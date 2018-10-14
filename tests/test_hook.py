import pytest
from pynextion.hardware import NexSerialMock
from pynextion.widgets import NexText
from pynextion.exceptions import NexException, NexIdException, NexNameException


def test_hook_by_code():
    nexSerial = NexSerialMock()

    # hook a page to nexSerial
    pagename = "pg_text"
    pid = 2
    page = nexSerial.components.hook_page(pagename, pid=pid)
    assert len(list(nexSerial.components.pages)) == 1

    # get page using name or pid
    returned_page = nexSerial.components.page(name=pagename)
    assert returned_page.name == pagename
    returned_page = nexSerial.components.page(pid=pid)
    assert returned_page.name == pagename
    # can't get a page by both name and pid
    with pytest.raises(NexException):
        nexSerial.components.page(name=pagename, pid=pid)

    # hook a widget (NexText) to a page
    nexText1 = page.hook_widget(NexText, "t1", cid=1)  # noqa
    assert len(list(page.widgets)) == 1
    # nexText1.text = "Hello"

    # hooked widgets must have unique name or cid (into associated page)
    with pytest.raises(NexNameException):
        page.hook_widget(NexText, "t1", cid=2)
    assert len(list(page.widgets)) == 1

    with pytest.raises(NexIdException):
        page.hook_widget(NexText, "t2", cid=1)
    assert len(list(page.widgets)) == 1

    # hook an other widget (NexText) to same page
    nexText2 = page.hook_widget(NexText, "t2", cid=2)   # noqa
    assert len(list(page.widgets)) == 2
    # nexText2.text = "World"

    # get widget using name or cid
    widget = page.widget(name="t1")
    assert widget.name == "t1"
    widget = page.widget(cid=1)
    assert widget.name == "t1"
    # can't get a widget by both name and cid
    with pytest.raises(NexException):
        page.widget(name="t1", cid=1)

    # hook a new page to nexSerial
    page = nexSerial.components.hook_page("pg_num", pid=7)
    assert len(list(nexSerial.components.pages)) == 2

    # page associated to nexserial must have unique name or cid (into associated page)
    with pytest.raises(NexNameException):
        nexSerial.components.hook_page("pg_num", pid=8)
    assert len(list(nexSerial.components.pages)) == 2

    with pytest.raises(NexIdException):
        nexSerial.components.hook_page("pg_num2", pid=7)
    assert len(list(nexSerial.components.pages)) == 2


def test_hook_by_data():
    nexSerial = NexSerialMock()

    pages = [
        {
            "pid": 2,
            "name": "pg_text",
            "components": [
                {
                    "type": "Text",
                    "cid": 2,
                    "name": "t0"
                },
                {
                    "type": "Text",
                    "cid": 3,
                    "name": "t1"
                },
                {
                    "type": "Text",
                    "cid": 1,
                    "name": "t2"
                }
            ]
        }
    ]

    # read pages/widget from data (pages variable)
    nexSerial.components.read_list(pages)

    # assert there is correct number of pages
    assert len(list(nexSerial.components.pages)) == 1

    # get a given page and assert it have correct number of widgets
    nexPage = nexSerial.components.page(name="pg_text")
    assert len(list(nexPage.widgets)) == 3

    # get a widget of this page using its name
    nexText = nexPage.widget(name="t1")
    assert isinstance(nexText, NexText)


# def test_hook_by_json_data():
#     pass
