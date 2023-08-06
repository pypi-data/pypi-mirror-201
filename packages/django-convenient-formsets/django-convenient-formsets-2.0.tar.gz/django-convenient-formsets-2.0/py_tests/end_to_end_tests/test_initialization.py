from urllib.parse import urlencode

from selenium.webdriver.common.by import By


def test_missing_options1(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    required options have not been specified.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_options_1.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Missing required options: "
        '"formsetPrefix", "formsContainerSelector", "formSelector", '
        '"addFormButtonSelector", "emptyFormTemplateSelector"'
    ]


def test_missing_options2(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    options that are conditionally required have not been specified.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_options_2.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Missing required options: "
        '"formsetPrefix", "formsContainerSelector", "formSelector", '
        '"addFormButtonSelector", "emptyFormTemplateSelector", '
        '"deleteFormButtonSelector", "moveFormDownButtonSelector", '
        '"moveFormUpButtonSelector"'
    ]


def test_missing_formset_elements1(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    required formset elements are missing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_formset_elements_1.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Unable to find DOM elements with selectors: "
        '"#formset #forms-container", "#formset #empty-form-template", '
        '"#formset #add-form-button"'
    ]


def test_missing_formset_elements2(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    the `deleteFormButtonSelector`, the `moveFormDownButtonSelector` and the
    `moveFormUpButtonSelector` cannot be found in the empty form.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_formset_elements_2.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Unable to find DOM elements in empty form template "
        'with selectors: "#delete-form-button", "#move-form-down-button", '
        '"#move-form-up-button", "input[name$="ORDER"]"'
    ]


def test_missing_formset_elements3(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    the `deleteFormButtonSelector`, the `moveFormDownButtonSelector` and the
    `moveFormUpButtonSelector` cannot be found in visible forms.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_formset_elements_3.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Unable to find DOM elements in one or more "
        'visible forms with selectors: "#delete-form-button", '
        '"#move-form-down-button", "#move-form-up-button", "input[name$="ORDER"]"'
    ]


def test_malformed_empty_form_template(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    the <template> element with `emptyFormTemplateSelector` contains more than
    1 child element.
    """
    # Load webpage for test
    params = {"template_name": "initialization/malformed_empty_form_template.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Expected 1 element inside "
        '"#formset #empty-form-template", found: 2'
    ]


def test_missing_management_form(live_server, selenium):
    """
    Asserts the ConvenientFormset instantiation raises an error message when
    the management form is missing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/missing_management_form.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == [
        "[ConvenientFormset] Management form for formset "
        'with prefix "formset" missing or has been tampered with.'
    ]


def test_hiding_forms_marked_for_deletion1(live_server, selenium):
    """
    ConvenientFormset has the `deleteFormButtonSelector` option set, hiding
    forms marked for deletion to be hidden when initializing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/hiding_deleted_forms_1.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == []

    # Assert that first form has `hidden` attribute set
    forms = selenium.find_elements(By.CSS_SELECTOR, "#formset #forms-container .form")
    assert len(forms) == 2

    assert forms[0].get_attribute("hidden") is not None
    assert forms[1].get_attribute("hidden") is None


def test_hiding_forms_marked_for_deletion2(live_server, selenium):
    """
    ConvenientFormset has the `deleteFormButtonSelector` option *NOT* set,
    leaving forms marked for deletion alone when initializing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/hiding_deleted_forms_2.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == []

    # Assert neither of the forms has the `hidden` attribute set
    forms = selenium.find_elements(By.CSS_SELECTOR, "#formset #forms-container .form")
    assert len(forms) == 2

    assert forms[0].get_attribute("hidden") is None
    assert forms[1].get_attribute("hidden") is None


def test_hiding_add_form_button_on_max_forms1(live_server, selenium):
    """
    ConvenientFormset has the `hideAddFormButtonOnMaxForms` option set to
    `true`, hiding the add form button when initializing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/hiding_add_form_button_1.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == []

    # Assert add form button does have the `hidden` attribute set
    add_form_button = selenium.find_element(
        By.CSS_SELECTOR, "#formset #add-form-button"
    )
    assert add_form_button.get_attribute("hidden") is not None


def test_hiding_add_form_button_on_max_forms2(live_server, selenium):
    """
    ConvenientFormset has the `hideAddFormButtonOnMaxForms` option set to
    `false`, leaving the add form button alone when initializing.
    """
    # Load webpage for test
    params = {"template_name": "initialization/hiding_add_form_button_2.html"}
    test_url = f"{live_server.url}?{urlencode(params)}"
    selenium.get(test_url)

    # Assert errors
    error_log = selenium.find_element(By.CSS_SELECTOR, "#error-log")
    error_messages = [msg.strip() for msg in error_log.text.split("\n") if msg.strip()]
    assert error_messages == []

    # Assert add form button does NOT have the `hidden` attribute set
    add_form_button = selenium.find_element(
        By.CSS_SELECTOR, "#formset #add-form-button"
    )
    assert add_form_button.get_attribute("hidden") is None
