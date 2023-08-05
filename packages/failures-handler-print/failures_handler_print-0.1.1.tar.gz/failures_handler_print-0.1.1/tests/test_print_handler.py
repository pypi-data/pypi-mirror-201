import re


def test_print_failure(capsys):
    from failures_handler_print import handler  # noqa

    handler("root.test_source.target", ValueError("test error"))
    sys_out = capsys.readouterr().out
    assert re.match(
        r".*\[FAILURE].*test_source.*::.*ValueError\(.*test error.*\).*\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.*",
        sys_out
    )


def test_integration_with_failures(capsys):
    import failures

    with failures.handle("test"):
        with failures.scope("sub"):
            with failures.scope("inner"):
                raise Exception("test error")
    assert re.match(
        r".*\[FAILURE].*test\.sub\.inner.*::.*Exception\(.*test error.*\).*\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.*",
        capsys.readouterr().out
    )
